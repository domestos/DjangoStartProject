from django.urls import path
from django.urls import include
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    path('', Home.as_view(), name='home_url' ),
    path('<int:pk>', Profile.as_view(), name='profile_url'),
    # path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='accounts/login.html'), name='login_url'),
    # redirect_authenticated_user=True  -redirect from the login page if a user was already authentication
    path('login/', Login.as_view(redirect_authenticated_user=True), name='login_url'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout_url"),
]

