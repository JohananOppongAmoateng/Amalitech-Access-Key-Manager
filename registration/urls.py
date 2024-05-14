"""
URLconf for registration and activation, using django-registration's
default backend.

If the default behavior of these views is acceptable to you, simply
use a line like this in your root URLconf to set up the default URLs
for registration::

    (r'^accounts/', include('registration.backends.default.urls')),

This will also automatically set up the views in
``django.contrib.auth`` at sensible default locations.

If you'd like to customize registration behavior, feel free to set up
your own URL patterns for these views instead.

"""
from django.urls import path
from django.views.generic.base import TemplateView

from .views import activate,register


urlpatterns = [
    path('activate/complete/',
         TemplateView.as_view(template_name='registration/activation_complete.html'),
         name='registration_activation_complete'),
    path('activate/<activation_key>/',
         activate,
         name='registration_activate'),
    path('register/complete/',
         TemplateView.as_view(template_name='registration/registration_complete.html'),
         name='registration_complete'),
        path('register/',
            register,
             name='register'),
]