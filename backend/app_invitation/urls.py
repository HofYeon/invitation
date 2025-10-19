from django.urls import path
from . import views
from .views import InvitationCreateView, InvitationCardView, GuestbookCreateAPIView, GuestbookDeleteAPIView

app_name = 'invitation'

urlpatterns = [

    path('create/', InvitationCreateView.as_view(), name='create'),
    path('card/<str:invitationname>/', InvitationCardView.as_view(), name='card'),
    path('holiday', views.holiday_view, name='holiday'),

    path('guestbooks/<int:invitation_id>/create/',GuestbookCreateAPIView.as_view(), name='guestbook_create'),
    path('guestbooks/<int:pk>/delete/', GuestbookDeleteAPIView.as_view(), name='guestbook_delete'),
]