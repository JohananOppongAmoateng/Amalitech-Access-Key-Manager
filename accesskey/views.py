from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import AccessKey
from .forms import CreateAccessKeyForm

@login_required(login_url="/accounts/login/")
def home(request):
    user = request.user
    if user.is_staff:
        keys = AccessKey.objects.all()
    
    else:
        keys =  AccessKey.objects.filter(user=user)
    context = {
        "keys" : keys
    }
    return render(request,"accesskey/home.html",context=context)



@login_required(login_url="/accounts/login/")
def create_access_key(request):
    if request.method == "POST":
        form = CreateAccessKeyForm(request.POST)
        if form.is_valid():
            user = request.user
            if not user.is_staff:
                active_key = AccessKey.objects.filter(user=user,status="active").exists()
                if active_key:
                    """give user feed back that they cant create new token because  they already have an active key and render home page with the feedback
                    """
                    messages.add_message(request,messages.INFO,"You already have an active key. You cannot create a new access key")
                    
                else:
                    new_key = form.save(commit=False)
                    new_key.user = user
                    new_key.save()
                    messages.add_message(request,messages.SUCCESS,f"Access key created successfully. Here is your new access key: {new_key.key}. Please copy it to a safe location you can only see it once")
            return render(request,"accesskey/home.html")
        
    else:
        form = CreateAccessKeyForm()
    context = {
        "form": form
    }
    return render(request,"accesskey/create_access_key.html",context=context)    

