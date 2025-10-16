from django.urls import path
from . import views
from .views import InvitationCreateView, InvitationCardView

app_name = 'invitation'

urlpatterns = [

    path('create/', InvitationCreateView.as_view(), name='create'),
    path('card/<int:invitation_id>/', InvitationCardView.as_view(), name='card'),
    path('holiday', views.holiday_view, name='holiday'),
]