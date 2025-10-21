from django.db.models import Prefetch, Count, F
from django.http import JsonResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, UpdateView, DetailView
from django.views import View
from django.utils import timezone

from .serializers import GuestbookSerializer

from .models import Invitation, InvitationFamily, Guestbook

from .forms import GuestbookForm


def is_filled(v):
    return bool(v and str(v).strip())


def full_name(last, first):
    last = (last or "").strip()
    first = (first or "").strip()
    return (last + first).strip() or None


class InvitationCreateView(CreateView):
    model = Invitation
    template_name = 'invitation/create.html'
    fields = ['user']
    success_url = '/invitation/preview/'

class InvitationCardView(View):

    def get(self, request, invitationname):
        # 1) families를 '신랑/신부'로 나눠서 미리 가져오기 (to_attr로 캐시에 저장)
        groom_prefetch = Prefetch(
            'families',
            queryset=InvitationFamily.objects.filter(side=InvitationFamily.Side.GROOM)
            .order_by('order', 'id'),
            to_attr='pref_groom_families'
        )
        bride_prefetch = Prefetch(
            'families',
            queryset=InvitationFamily.objects.filter(side=InvitationFamily.Side.BRIDE)
            .order_by('order', 'id'),
            to_attr='pref_bride_families'
        )

        # 2) 방명록도 미리(prefetch) 최신순/필요필드만 가져오기
        guestbook_prefetch = Prefetch(
            'guestbook_entries',  # 모델에서 related_name='guestbook_entries'라고 가정
            queryset=Guestbook.objects.only('id', 'author_name', 'content', 'created_at')
            .order_by('-created_at'),
            to_attr='pref_guestbook_entries'
        )

        # 3) 단일 FK는 select_related, M2M/역참조는 prefetch_related
        invitation = get_object_or_404(
            Invitation.objects
            .select_related('greeting', 'calendar', 'map')
            .prefetch_related(groom_prefetch, bride_prefetch, guestbook_prefetch, 'gallery')
            .annotate(guestbook_count=Count('guestbook_entries')),  # 필요하면 카운트도 한 번에
            invitationname=invitationname
        )

        invitation.count = F('count') + 1
        invitation.save(update_fields=['count'])
        # invitation.refresh_from_db(fields=['count'])

        #계좌 분리
        # --- 신랑 측 ---
        groom_accounts = []
        if is_filled(getattr(invitation, "groom_account", None)):
            groom_accounts.append({
                "label": "main",
                "role": "couple",
                "bank":invitation.groom_bankname.strip(),  # 필요 시 Invitation에 은행명 필드가 있으면 채우세요
                "account": invitation.groom_account.strip(),
                "holder": full_name(invitation.groom_lastname, invitation.groom_firstname),
            })

        groom_family = (invitation.pref_groom_families[0] if getattr(invitation, "pref_groom_families", None) else None)
        if groom_family:
            if groom_family and is_filled(getattr(groom_family, "father_account", None)):
                groom_accounts.append({
                    "label": "family",
                    "role": "father",
                    "bank": (groom_family.father_bankname or "").strip() or None,
                    "account": groom_family.father_account.strip(),
                    "holder": full_name(groom_family.father_last_name, groom_family.father_first_name),
                })
            if groom_family and is_filled(getattr(groom_family, "mother_account", None)):
                groom_accounts.append({
                    "label": "family",
                    "role": "mother",
                    "bank": (groom_family.mother_bankname or "").strip() or None if hasattr(groom_family,
                                                                                            "mother_bankname") else None,
                    "account": groom_family.mother_account.strip(),
                    "holder": full_name(
                        getattr(groom_family, "mother_last_name", None),
                        getattr(groom_family, "mother_first_name", None),
                    ),
                })

        # --- 신부 측 ---
        bride_accounts = []
        if is_filled(getattr(invitation, "bride_account", None)):
            bride_accounts.append({
                "label": "main",
                "role": "couple",
                "bank": invitation.bride_bankname.strip(),  # 필요 시 Invitation에 은행명 필드가 있으면 채우세요
                "account": invitation.bride_account.strip(),
                "holder": full_name(invitation.bride_lastname, invitation.bride_firstname),
            })

        bride_family = (
            invitation.pref_bride_families[0] if getattr(invitation, "pref_bride_families", None) else None)
        if bride_family:
            if bride_family and is_filled(getattr(bride_family, "father_account", None)):
                bride_accounts.append({
                    "label": "family",
                    "role": "father",
                    "bank": (bride_family.father_bankname or "").strip() or None,
                    "account": bride_family.father_account.strip(),
                    "holder": full_name(bride_family.father_last_name, bride_family.father_first_name),
                })
            if bride_family and is_filled(getattr(bride_family, "mother_account", None)):
                bride_accounts.append({
                    "label": "family",
                    "role": "mother",
                    "bank": (bride_family.mother_bankname or "").strip() or None if hasattr(bride_family,
                                                                                            "mother_bankname") else None,
                    "account": bride_family.mother_account.strip(),
                    "holder": full_name(
                        getattr(bride_family, "mother_last_name", None),
                        getattr(bride_family, "mother_first_name", None),
                    ),
                })


        # 날짜 처리
        dt = timezone.localtime(invitation.wedding_datetime)
        weekday_upper = dt.strftime('%A').upper()

        # 여기서 추가 DB쿼리 없음 (to_attr 덕분)
        groom_families = getattr(invitation, 'pref_groom_families', [])
        bride_families = getattr(invitation, 'pref_bride_families', [])
        guestbooks = getattr(invitation, 'pref_guestbook_entries', [])  # 최신순 이미 적용됨
        gallery = invitation.gallery.all()  # prefetch로 이미 캐시됨, 추가쿼리 X


        # 2️⃣ 템플릿에 넘길 context 구성
        context = {
            "invitation": invitation,
            "greeting": getattr(invitation, "greeting", None),
            "groom_families": groom_families,
            "bride_families": bride_families,
            "calendar": getattr(invitation, "calendar", None),
            "gallery": gallery,
            "map": getattr(invitation, "map", None),
            "weekday_upper": weekday_upper,
            "guestbooks" : guestbooks,
            "bride_accounts" : bride_accounts,
            "groom_accounts" : groom_accounts,
        }

        return render(request, 'invitation/invitation_card.html', context)

    
def holiday_view(request):
    date = request.GET.get("date")  # AJAX에서 보낸 date=2025-11-22
    # 예시 데이터 — 실제론 DB 조회나 로직을 여기에 넣으면 됨
    data = [
    ]

    return JsonResponse(data, safe=False)

class GuestbookCreateAPIView(generics.CreateAPIView):
    """
    POST /api/invitations/<invitation_id>/guestbook-entries/
    Body: { author_name, content, raw_password }
    """
    serializer_class = GuestbookSerializer
    permission_classes = [permissions.AllowAny]
    def perform_create(self, serializer):
        invitation = get_object_or_404(Invitation, pk=self.kwargs['invitation_id'])
        serializer.save(invitation=invitation)


class GuestbookDeleteAPIView(generics.DestroyAPIView):
    """
    DELETE /api/guestbook-entries/<pk>/
    Body: { password: "..." }  # 비밀번호 확인용
    """
    queryset = Guestbook.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = GuestbookSerializer  # 읽기는 안 쓰지만 형식상 지정

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        password = request.data.get('password', '')  # jQuery에서 data로 보냄
        print(password)
        print('-----------------------')
        if instance.check_password(password):
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': '비밀번호가 올바르지 않습니다.'}, status=status.HTTP_403_FORBIDDEN)