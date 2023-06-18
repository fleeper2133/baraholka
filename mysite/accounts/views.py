from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView
from .forms import *
from articles.models import Articles


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')
    extra_context = {'title': "Регистрация"}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('profile')


class UserProfile(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'accounts/user_profile.html'
    extra_context = {'title': 'Профиль'}


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'accounts/login.html'
    extra_context = {'title': "Авторизация"}

    def get_success_url(self):
        return reverse_lazy('profile')


def logout_user(request):
    logout(request)
    return redirect('login')


class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = Articles.objects.values('title', 'acceptance_stage', 'user').filter(user=self.request.user.pk)
        context['articles'] = articles
        context['title'] = "Профиль"
        return context


@login_required
@transaction.atomic
def profile_update(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
        else:
            messages.error(request, 'Ошибка!')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/profile_update.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': "Обновление информации"
    })
