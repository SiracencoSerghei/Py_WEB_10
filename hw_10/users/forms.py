from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("email",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = None

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if get_user_model().objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter username"}
        ),
    )
    email = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter email"}
        ),
    )

    password1 = forms.CharField(
        label="Password",
        required=True,
        min_length=8,
        max_length=25,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
    )

    password2 = forms.CharField(
        label="Password confirmation",
        required=True,
        min_length=8,
        max_length=25,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter username"}
        ),
    )
    password = forms.CharField(
        max_length=25,
        min_length=8,
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "password",
        ]


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control"}))

    class Meta:
        model = Profile
        fields = ["avatar"]



class DeleteForm(forms.ModelForm):
    username = forms.CharField(
        max_length=100, required=True, widget=forms.HiddenInput()
    )

    class Meta:
        model = User
        fields = [
            "username",
        ]

