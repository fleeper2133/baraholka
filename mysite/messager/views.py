from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .forms import MessageForm
from .models import *


def delete_duplicates_profiles(profiles: list, pk_user: int) -> list:
    check = []
    new_profiles = []
    for profile in profiles:
        if profile.sender.id != pk_user:
            if profile.sender.id not in check:
                new_profiles.append(profile)
                check.append(profile.sender.id)

        elif profile.recipient.id != pk_user:
            if profile.recipient.id not in check:
                new_profiles.append(profile)
                check.append(profile.recipient.id)

    return new_profiles


class ProfilesMessage(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messager/messager_profiles.html'
    context_object_name = 'profiles_message'
    extra_context = {'title': "Сообщения"}
    login_url = 'login'

    def get_queryset(self):
        profiles = Message.objects.filter(
            Q(sender_id=self.request.user.pk) | Q(recipient_id=self.request.user.pk)
        ).select_related('sender', 'recipient').order_by('-time_create')\
            .prefetch_related('sender__profile')

        new_profiles = delete_duplicates_profiles(profiles, self.request.user.pk)

        return new_profiles


@login_required(login_url='login')
def get_messages(request, pk):

    if request.POST:
        form = MessageForm(request.POST, request.FILES)
        form.instance.sender_id = request.user.pk
        form.instance.recipient_id = pk
        if form.is_valid():
            form.save()

    form = MessageForm()

    messages = Message.objects.filter(
        Q(sender_id=pk, recipient_id=request.user.pk) | Q(recipient_id=pk, sender_id=request.user.id)
    ).select_related('sender').prefetch_related('sender__profile')

    profiles = Message.objects.filter(
        Q(sender_id=request.user.pk) | Q(recipient_id=request.user.pk)
    ).select_related('sender', 'recipient').order_by('-time_create')\
        .prefetch_related('sender__profile', 'recipient__profile')

    new_profiles = delete_duplicates_profiles(profiles, request.user.pk)
    user_sender = User.objects.get(pk=pk)

    data = {
        'title': "Сообщения",
        "messages": messages,
        "profiles_message": new_profiles,
        "pk_selected": pk,
        "form": form,
        "user_sender": user_sender
    }

    return render(request, 'messager/messager.html', data)

