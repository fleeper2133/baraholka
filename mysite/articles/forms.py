from django import forms
from .models import *


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ('cat', 'title', 'content', 'photo')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'cat': forms.RadioSelect(attrs={'class': 'form-check-input flex-shrink-0'})
        }