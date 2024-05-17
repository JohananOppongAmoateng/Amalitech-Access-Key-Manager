from django.contrib.auth.forms import BaseUserCreationForm
from .models import CustomUser
class SignUpForm(BaseUserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["email","password1","password2"]