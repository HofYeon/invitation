from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DetailView
from .models import Invitation

class InvitationCreateView(CreateView):
    model = Invitation
    template_name = 'invitation/create.html'
    fields = ['user']
    success_url = '/invitation/preview/'

    
