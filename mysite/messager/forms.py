from django import forms
from .models import *


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('message', 'photo')
        widgets = {
            'message': forms.TextInput(attrs={"class": "form-control form-control-lg",
                                              "placeholder": "Напиши сообщение"}),
            'photo': forms.FileInput(attrs={"id": "file_b"})
        }
