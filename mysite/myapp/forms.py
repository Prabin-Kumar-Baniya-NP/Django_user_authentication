from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms


class SignupForm(UserCreationForm):
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'email': "Email Address",
        }


class EditUserProfile(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "date_joined", "last_login"]
        labels = {
            'email': "Email Address",
        }


class EditAdminProfile(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = '__all__'
        labels = {
            'email': "Email Address",
        }
