from django.contrib import admin
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import (
    Invitation,
    InvitationGreeting,
    InvitationFamily,
    InvitationCalendar,
    InvitationGallery,
    InvitationMap,
    Guestbook,
)

# ---------------------------
# 기본 Invitation
# ---------------------------
@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "groom_lastname",
        "groom_firstname",
        "bride_lastname",
        "bride_firstname",
        "wedding_datetime",
        "weddinghall_name",
        "created_at",
    )
    search_fields = (
        "groom_lastname",
        "groom_firstname",
        "bride_lastname",
        "bride_firstname",
        "weddinghall_name",
    )
    list_filter = ("wedding_datetime", "created_at")


# ---------------------------
# 모시는 글
# ---------------------------
class GreetingForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditor5Widget(config_name='default'))
    class Meta:
        model = InvitationGreeting
        fields = '__all__'

@admin.register(InvitationGreeting)
class GreetingAdmin(admin.ModelAdmin):
    form = GreetingForm


# ---------------------------
# 가족 소개
# ---------------------------
@admin.register(InvitationFamily)
class InvitationFamilyAdmin(admin.ModelAdmin):
    list_display = ("id", "invitation", "side", "father_last_name", "mother_last_name")
    list_filter = ("side",)
    search_fields = ("father_last_name", "mother_last_name")
    raw_id_fields = ("invitation",)


# ---------------------------
# 캘린더
# ---------------------------
@admin.register(InvitationCalendar)
class InvitationCalendarAdmin(admin.ModelAdmin):
    list_display = ("id", "invitation")
    raw_id_fields = ("invitation",)


# ---------------------------
# 갤러리
# ---------------------------
@admin.register(InvitationGallery)
class InvitationGalleryAdmin(admin.ModelAdmin):
    list_display = ("id", "invitation", "image", "order", "createdate")
    list_filter = ("createdate",)
    raw_id_fields = ("invitation",)


# ---------------------------
# 지도/주소
# ---------------------------
@admin.register(InvitationMap)
class InvitationMapAdmin(admin.ModelAdmin):
    list_display = ("id", "invitation", "address", "building_name", "sido", "sigungu")
    search_fields = ("address", "building_name", "roadname")
    list_filter = ("sido", "sigungu")
    raw_id_fields = ("invitation",)

class GuestbookInline(admin.TabularInline):
    model = Guestbook
    extra = 0
    can_delete = True
    ordering = ('-created_at',)
    readonly_fields = ('author_name', 'content', 'created_at', 'password')  # 해시 비번은 노출 X
    fields = ('author_name', 'content','password', 'created_at')

# ---- 방명록 전용 리스트 화면 ----
@admin.register(Guestbook)
class GuestbookAdmin(admin.ModelAdmin):
    list_display = ('id', 'invitation', 'author_name', 'created_at', 'content_preview')
    list_filter = ('invitation', 'created_at')
    search_fields = ('author_name', 'content')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('invitation', 'author_name', 'content', 'created_at', 'password')  # 비밀번호 해시 노출 X
    # 보여줄 필드 순서(상단 상세 패널)
    fields = ('invitation', 'author_name', 'password', 'content', 'created_at')

    def content_preview(self, obj):
        # 이모지 그대로 보이고 40자만 미리보기
        text = (obj.content or '')
        return (text[:40] + '…') if len(text) > 40 else text
    content_preview.short_description = '내용(미리보기)'
