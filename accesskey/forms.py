from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import AccessKey

class CreateAccessKeyForm(forms.ModelForm):
    class Meta:
        model =  AccessKey
        fields = ['name']
