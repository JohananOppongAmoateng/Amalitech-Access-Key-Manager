"""
Forms and validation code for user registration.

Note that all of these forms assume Django's bundle default ``User``
model; since it's not possible for a form to anticipate in advance the
needs of custom user models, you will need to write your own forms if
you're using a custom model.

"""
from django import forms
from django.contrib.auth.forms import BaseUserCreationForm
from .models import CustomUser
from django import forms
from django.utils.translation import gettext_lazy as _


class RegistrationForm(BaseUserCreationForm):
   
    required_css_class = 'required'
    email = forms.EmailField(label=_("E-mail"))

    class Meta:
        model = CustomUser
        fields = ("email","password1","password2")


class ResendActivationForm(forms.Form):
    required_css_class = 'required'
    email = forms.EmailField(label=_("E-mail"))


