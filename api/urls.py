from django.urls import path
from .views import get_access_key_details_with_email


urlpatterns = [
    path("key/<str:email>",get_access_key_details_with_email,name="active-key-detail")
]