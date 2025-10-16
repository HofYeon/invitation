from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView, DetailView
from django.views import View
from django.utils import timezone

from .models import Invitation, InvitationFamily

class InvitationCreateView(CreateView):
    model = Invitation
    template_name = 'invitation/create.html'
    fields = ['user']
    success_url = '/invitation/preview/'

class InvitationCardView(View):
    def get(self, request, invitation_id):

        invitation = get_object_or_404(
            Invitation.objects.select_related(
                "greeting", "calendar", "map"
            ).prefetch_related(
                Prefetch("families", queryset=InvitationFamily.objects.order_by("order", "id")),"gallery"
            ),
            id=invitation_id
        )

        dt = timezone.localtime(invitation.wedding_datetime)
        weekday_upper = dt.strftime("%A").upper()

        groom_families = invitation.families.filter(side=InvitationFamily.Side.GROOM)  # 1
        bride_families = invitation.families.filter(side=InvitationFamily.Side.BRIDE)
        print('        ')
        print(groom_families)
        print('       -------------------- ')
        # 2️⃣ 템플릿에 넘길 context 구성
        context = {
            "invitation": invitation,
            "greeting": getattr(invitation, "greeting", None),
            "groom_families": groom_families,
            "bride_families": bride_families,
            "calendar": getattr(invitation, "calendar", None),
            "gallery": invitation.gallery.all(),
            "map": getattr(invitation, "map", None),
            "weekday_upper": weekday_upper,
        }

        return render(request, 'invitation/invitation_card.html', context)

    
def holiday_view(request):
    date = request.GET.get("date")  # AJAX에서 보낸 date=2025-11-22
    print("받은 날짜:", date)

    # 예시 데이터 — 실제론 DB 조회나 로직을 여기에 넣으면 됨
    data = [
        {"day":4},
        {"day": 9},
        {"day": 16},
        {"day": 23},
        {"day":28},
    ]
    print(data)

    return JsonResponse(data, safe=False)