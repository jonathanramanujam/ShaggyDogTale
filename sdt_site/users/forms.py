from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.fields import EmailField
from django.forms.forms import Form

class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Username', min_length=5, max_length=150)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def username_clean(self):
        username = self.cleaned_data['Username'].lower()
        new = User.objects.filter(username = username)
        if new.count():
            raise ValidationError("User already exists")
        return username

    def email_clean(self):
        email = self.cleaned_data['Email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")
        return password2

    def save(self, commit = True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user
