from django import forms
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget
from django.core.exceptions import ValidationError

from .models import Posts
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import re


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class PostsForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    picture = forms.ImageField()
    title = 'Написать пост'

    class Meta:
        model = Posts
        fields = ['title', 'description', 'content', 'picture', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),

        }

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        for i in tags:
            if re.match(r'[А-Я]\w+', i):
                raise ValidationError("Русские теги тут не позволительны!")
            else:
                return tags
