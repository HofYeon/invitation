from django.urls import path
from .views import InvitationCreateView

app_name = 'invitation'

urlpatterns = [

    path('create/', InvitationCreateView.as_view(), name='create'),
]