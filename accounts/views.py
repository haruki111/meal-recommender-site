from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.account import views
from .models import CustomUser
from .forms import ProfileForm, SignupUserForm, LoginUserForm
# Create your views here.


class SignupView(views.SignupView):
    template_name = 'registration/signup.html'
    form_class = SignupUserForm


class LoginView(views.LoginView):
    template_name = 'registration/login.html'
    form_class = LoginUserForm


class ProfileView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        return render(self.request, 'registration/profile.html')


class ProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = 'registration/profile_edit.html'
    model = CustomUser
    form_class = ProfileForm
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user
