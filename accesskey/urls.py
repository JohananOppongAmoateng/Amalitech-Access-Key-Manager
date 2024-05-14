
from django.urls import path
from .views import home, create_access_key
urlpatterns = [
    path('', home, name='home'),
    path('create/', create_access_key, name='create_access_key'),
]