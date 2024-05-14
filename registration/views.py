"""
Views which allow users to create and activate accounts.

""" 
from django.shortcuts import render, redirect
from .models  import AccountVerification
from django.shortcuts import redirect
from .forms import RegistrationForm
from django.views.decorators.http import require_http_methods
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login



@require_http_methods(["GET","POST"])
def register(request):
    if request.method == "GET":
        form =  RegistrationForm()
        return render(request,"registration/register.html",{"form":form})
    else:
        form =  RegistrationForm(request.POST)
        if form.is_valid():
            site = get_current_site(request)
            new_user_instance = form.save(commit=False)
            new_user = AccountVerification.objects.create_inactive_user(
                new_user=new_user_instance,
                site=site,
                send_email=True,
                request=request,
        )
            return redirect('registration_complete')
        

@require_http_methods(["GET"])
def activate(request,activation_key):
    site = get_current_site(request)
    user, activated = AccountVerification.objects.activate_user(
            activation_key)
    if activated:
        login(request, user)
        return redirect('registration_activation_complete')