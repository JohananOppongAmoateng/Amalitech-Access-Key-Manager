from django.urls import path
from .views import SignUpView, ActivateAccount
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='register'),

    path('activate/<token>/', ActivateAccount.as_view(), name='registration_activate'),
]