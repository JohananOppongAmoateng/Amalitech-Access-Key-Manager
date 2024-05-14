from django.urls import path
from .api_view import get_access_key_details_with_email


urlpatterns = [
    path("key/<str:school_email>",get_access_key_details_with_email,name="active-key-detail")
]