from django.shortcuts import render
from django.views import View
from .models import User
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView   
from django.contrib import messages
from config.custom_exeptions import ExeptionHunter
import logging

logger = logging.getLogger('ExeptionHunter')

class Login(LoginView):
    template_name = 'accounts/login.html'
        
class Home(LoginRequiredMixin, ExeptionHunter):
    """ Class ExeptionHunter is extended by View """
    def get(self, request):
        return render(request, 'accounts/home.html', context={})

class Profile(LoginRequiredMixin, ExeptionHunter):
    def get(self, request, pk):
        logger.info('Walcome, '+str(request.user))
        messages.success(request,'Walcome, '+str(request.user), extra_tags="alert-success") 
        user = get_object_or_404(User, pk=pk)
        return render(request, 'accounts/profile.html', context={'user':user})

