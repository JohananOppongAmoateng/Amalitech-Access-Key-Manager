from django.contrib import admin
from .models import CustomUser,ActivationToken

admin.site.register(CustomUser)
admin.site.register(ActivationToken)