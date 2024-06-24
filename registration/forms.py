from django.contrib.auth.forms import BaseUserCreationForm,UserChangeForm
from .models import CustomUser


class SignUpForm(BaseUserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["email","password1","password2"]


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)