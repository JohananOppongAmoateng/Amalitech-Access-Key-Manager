# Create your models here.
import datetime
import hashlib
import logging
import re
import string

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils.timezone import now as datetime_now
from django.db import models
from django.db import transaction
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMultiAlternatives


logger = logging.getLogger(__name__)

# Adding some backwards compatibility for SHA1
# The 40 probably should be removed later on
SHA256_RE = re.compile('^[a-f0-9]{40,64}$')



def get_from_email(site=None):
    """
    Return the email address by which mail is sent.
    If the `REGISTRATION_USE_SITE_EMAIL` setting is set, the `Site` object will
    provide the domain and the REGISTRATION_SITE_USER_EMAIL will provide the
    username. Otherwise the `REGISTRATION_DEFAULT_FROM_EMAIL` or
    `DEFAULT_FROM_EMAIL` settings are used.
    """
    if getattr(settings, 'REGISTRATION_USE_SITE_EMAIL', False):
        user_email = getattr(settings, 'REGISTRATION_SITE_USER_EMAIL', None)
        if not user_email:
            raise ImproperlyConfigured((
                'REGISTRATION_SITE_USER_EMAIL must be set when using '
                'REGISTRATION_USE_SITE_EMAIL.'))
        Site = apps.get_model('sites', 'Site')
        site = site or Site.objects.get_current()
        from_email = '{}@{}'.format(user_email, site.domain)
    else:
        from_email = getattr(settings, 'REGISTRATION_DEFAULT_FROM_EMAIL',
                             settings.DEFAULT_FROM_EMAIL)
    return from_email


def send_email(addresses_to, ctx_dict, subject_template, body_template,
               body_html_template):
    """
    Function that sends an email
    """

    prefix = getattr(settings, 'REGISTRATION_EMAIL_SUBJECT_PREFIX', '')
    subject = prefix + render_to_string(subject_template, ctx_dict)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    from_email = get_from_email(ctx_dict.get('site'))
    message_txt = render_to_string(body_template,
                                   ctx_dict)

    email_message = EmailMultiAlternatives(subject, message_txt,
                                           from_email, addresses_to)

    if getattr(settings, 'REGISTRATION_EMAIL_HTML', True):
        try:
            message_html = render_to_string(
                body_html_template, ctx_dict)
        except TemplateDoesNotExist:
            pass
        else:
            email_message.attach_alternative(message_html, 'text/html')

    email_message.send()




class CustomUser(AbstractUser):
    """
    Custom User Model 
        This model uses email logs in with email and password
    """
    email = models.EmailField(unique=True,blank=False,null=False,error_messages={
            "unique": "A user with that email already exists.",
        },)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []





class AccountVerificationManager(models.Manager):
    """
    Custom manager for the ``AccountVerification`` model.

    The methods defined here provide shortcuts for account creation
    and activation (including generation and emailing of activation
    keys).

    """

    def _activate(self, profile):
        """
        Activate the ``AccountVerification`` given as argument.
        User is able to login, as ``is_active`` is set to ``True``
        """
        user = profile.user
        user.is_active = True
        profile.activated = True

        with transaction.atomic():
            user.save()
            profile.save()
            return user

    def activate_user(self, activation_key):
        """
        Validate an activation key and activate the corresponding ``User`` if
        valid, returns a tuple of (``User``, ``activated``). The activated flag
        indicates if the user was newly activated or an error occurred.

        If the key is valid and has not expired, return the (``User``,
        ``True``) after activating.

        If the key is not valid or has expired, return (``User`` or ``False``,
        ``False``).

        If the key is valid but the ``User`` is already active,
        return (``User``, ``False``).

        If the key is valid but the ``User`` is inactive, return (``User``,
        ``False``).

        To prevent reactivation of an account which has been
        deactivated by site administrators, ``AccountVerification.activated``
        is set to ``True`` after successful activation.

        """
        # Make sure the key we're trying conforms to the pattern of a
        # SHA256 hash; if it doesn't, no point trying to look it up in
        # the database.
        # The or statement is used
        if SHA256_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                # This is an actual activation failure as the activation
                # key does not exist. It is *not* the scenario where an
                # already activated User reuses an activation key.
                return (False, False)

            if profile.activated:
                # The User has already activated and is trying to activate
                # again. If the User is active, return the User. Else,
                # return False as the User has been deactivated by a site
                # administrator.
                return (profile.user, False)

            if not profile.activation_key_expired():
                return (self._activate(profile), True)

        return (False, False)

    def create_inactive_user(self, site, new_user=None, send_email=True,
                             request=None, profile_info={}, **user_info):
        """
        Create a new, inactive ``User``, generate a
        ``AccountVerification`` and email its activation key to the
        ``User``, returning the new ``User``.

        By default, an activation email will be sent to the new
        user. To disable this, pass ``send_email=False``.
        Additionally, if email is sent and ``request`` is supplied,
        it will be passed to the email template.

        """
        if new_user is None:
            password = user_info.pop('password')
            new_user = CustomUser(**user_info)
            new_user.set_password(password)
        new_user.is_active = False

        # Since we calculate the AccountVerification expiration from this date,
        # we want to ensure that it is current
        new_user.date_joined = datetime_now()

        with transaction.atomic():
            new_user.save()
            registration_profile = self.create_profile(
                new_user, **profile_info)

            # send email only if desired and transaction succeeds
            if send_email:
                transaction.on_commit(
                    lambda: registration_profile.send_activation_email(
                        site, request)
                )

        return new_user

    def create_profile(self, user, **profile_info):
        """
        Create a ``AccountVerification`` for a given
        ``User``, and return the ``AccountVerification``.

        The activation key for the ``AccountVerification`` will be a
        SHA256 hash, generated from a secure random string.

        """
        profile = self.model(user=user, **profile_info)

        if 'activation_key' not in profile_info:
            profile.create_new_activation_key(save=False)

        profile.save()

        return profile

    

class AccountVerification(models.Model):
    """
    A simple model which stores an activation key for use during
    user account registration.

    Generally, you will not want to interact directly with instances
    of this model; the provided manager includes methods
    for creating and activating new accounts, as well as for cleaning
    out accounts which have never been activated.

    While it is possible to use this model as the value of the
    ``AUTH_PROFILE_MODULE`` setting, it's not recommended that you do
    so. This model's sole purpose is to store data temporarily during
    account registration and activation.

    """

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,

    )
    activation_key = models.CharField(max_length=64)
    activated = models.BooleanField(default=False)

    objects = AccountVerificationManager()

    def __str__(self):
        return "Registration information for %s" % self.user

    def create_new_activation_key(self, save=True):
        """
        Create a new activation key for the user
        """
        random_string = get_random_string(
            length=32, allowed_chars=string.printable)
        self.activation_key = hashlib.sha256(
            random_string.encode()).hexdigest()

        if save:
            self.save()

        return self.activation_key

    def activation_key_expired(self):
       
        max_expiry_days = datetime.timedelta(
            days=settings.ACCOUNT_ACTIVATION_DAYS)
        expiration_date = self.user.date_joined + max_expiry_days
        return self.activated or expiration_date <= datetime_now()

    def send_activation_email(self, site, request=None):
        
        activation_email_subject = getattr(settings, 'ACTIVATION_EMAIL_SUBJECT',
                                           'registration/activation_email_subject.txt')
        activation_email_body = getattr(settings, 'ACTIVATION_EMAIL_BODY',
                                        'registration/activation_email.txt')
        activation_email_html = getattr(settings, 'ACTIVATION_EMAIL_HTML',
                                        'registration/activation_email.html')

        ctx_dict = {
            'user': self.user,
            'activation_key': self.activation_key,
            'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
            'site': site,
        }
        prefix = getattr(settings, 'REGISTRATION_EMAIL_SUBJECT_PREFIX', '')
        subject = prefix + render_to_string(
            activation_email_subject, ctx_dict, request=request
        )

        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        from_email = get_from_email(site)
        message_txt = render_to_string(activation_email_body,
                                       ctx_dict, request=request)

        email_message = EmailMultiAlternatives(subject, message_txt,
                                               from_email, [self.user.email])

        if getattr(settings, 'REGISTRATION_EMAIL_HTML', True):
            try:
                message_html = render_to_string(
                    activation_email_html, ctx_dict, request=request)
            except TemplateDoesNotExist:
                pass
            else:
                email_message.attach_alternative(message_html, 'text/html')

        email_message.send()



    