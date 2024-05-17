from django.shortcuts import render
from django.views import View
from .models import CustomUser,ActivationToken
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import TemplateView
from .forms import SignUpForm


class SignUpView(View):
    form = SignUpForm
    template_name = 'registration/register.html'

    def get(self, request):
        form = self.form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            user = CustomUser.objects.create_user(email=form.cleaned_data['email'], password=form.cleaned_data['password1'],is_active = False)
            user.save()
            token = ActivationToken.objects.create(user=user)
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'site': current_site,
                'domain': current_site.domain,
                'token': token,
            })
            send_mail(mail_subject, message, None, [user.email])
            return render(request, 'registration/registration_complete.html')
        return render(request, self.template_name, {'form': form})

class ActivateAccount(TemplateView):
    http_method_names = ['get']
    template_name = 'registration/activate.html'
    def get(self,request,token):
        try:
            token = ActivationToken.objects.get(token=token)
            if not token.activated:
                token.activated = True
                token.user.is_active = True
                token.user.save()
                token.save()
                return render(request, "registration/activation_complete.html", {'message': 'Account activated'})
                
            return render(request, "registration/activation_complete.html", {'message': 'Account already activated'})
        except ActivationToken.DoesNotExist:
            return render(request, self.template_name, {'message': 'Invalid token'})
        