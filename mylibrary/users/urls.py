from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView, ProfileView
from .forms import CustomAuthenticationForm

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', auth_views.LoginView.as_view(authentication_form=CustomAuthenticationForm), name='login'),
]