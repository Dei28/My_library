from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from .forms import CustomUserCreationForm  # импортируем нашу форму

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm  # изменено
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return self.request.user