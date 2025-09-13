from django.db import models
from django.conf import settings

# Create your models here
class Invitation(models.Model):
    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_invitations" )
    groom_lastname = models.CharField("신랑 성", max_length=100)
    groom_firstname = models.CharField("신랑 이름", max_length=100)
    bride_lastname = models.CharField("신부 성", max_length=100)
    bride_firstname = models.CharField("신부 이름", max_length=100)
    wedding_datetime = models.DateTimeField("결혼식 날짜")
    weddinghall_name = models.CharField("결혼식장 이름", max_length=100)
    weddinghall_info = models.CharField("웨딩홀 정보", max_length=200)
    created_at = models.DateTimeField("생성일", auto_now_add=True)
    update_at = models.DateTimeField("수정일", auto_now = True)
