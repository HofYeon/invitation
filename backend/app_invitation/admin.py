from django.contrib import admin
from .models import (
    Invitation,
    InvitationGreeting,
    InvitationFamily,
    InvitationCalendar,
    InvitationGallery,
    InvitationMap,
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
@admin.register(InvitationGreeting)
class InvitationGreetingAdmin(admin.ModelAdmin):
    list_display = ("id", "invitation", "title", "subtitle")
    search_fields = ("title", "subtitle", "body")
    raw_id_fields = ("invitation",)


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
