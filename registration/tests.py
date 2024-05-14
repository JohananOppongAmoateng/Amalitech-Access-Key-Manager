
# Create your tests here.
import datetime

from django.conf import settings
from django.core import mail
from django.db import DatabaseError
from django.test import TransactionTestCase
from django.urls import reverse
from registration.forms import RegistrationForm
from registration.models import AccountVerification,CustomUser
from registration.views import register


class RegisterationViewTests(TransactionTestCase):
    """
    Test the default registration backend.

    Running these tests successfully will require two templates to be
    created for the sending of activation emails; details on these
    templates and their contexts may be found in the documentation for
    the default backend.

    """

    account_verification = AccountVerification()

    registration_view = register


    def test_registration_get(self):
        """
        HTTP ``GET`` to the registration view uses the appropriate
        template and populates a registration form into the context.

        """
        resp = self.client.get(reverse('registration_register'))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp,
                                'registration/registration_form.html')
        self.assertIsInstance(resp.context['form'], RegistrationForm)

    def test_registration(self):
        """
        Registration creates a new inactive account and a new profile
        with activation key, populates the correct account data and
        sends an activation email.

        """
        resp = self.client.post(reverse('registration_register'),
                                data={'username': 'bob',
                                      'email': 'bob@example.com',
                                      'password1': 'secret',
                                      'password2': 'secret'})
        self.assertRedirects(resp, reverse('registration_complete'))

        new_user = CustomUser().objects.get(username='bob')

        self.assertTrue(new_user.check_password('secret'))
        self.assertEqual(new_user.email, 'bob@example.com')

        # New user must not be active.
        self.assertFalse(new_user.is_active)

        # A registration profile was created, and an activation email
        # was sent.
        self.assertEqual(self.account_verification.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

        
    def test_registration_failure(self):
        """
        Registering with invalid data fails.

        """
        resp = self.client.post(reverse('registration_register'),
                                data={'username': 'bob',
                                      'email': 'bob@example.com',
                                      'password1': 'secret',
                                      'password2': 'notsecret'})
        self.assertEqual(200, resp.status_code)
        self.assertFalse(resp.context['form'].is_valid())
        self.assertEqual(0, len(mail.outbox))

    def test_activation(self):
        """
        Activation of an account functions properly.

        """
        resp = self.client.post(reverse('registration_register'),
                                data={'username': 'bob',
                                      'email': 'bob@example.com',
                                      'password1': 'secret',
                                      'password2': 'secret'})

        profile = self.account_verification.objects.get(user__username='bob')

        resp = self.client.get(
            reverse('registration_activate',
                    args=(),
                    kwargs={'activation_key': profile.activation_key}))
        self.assertRedirects(resp, reverse('registration_activation_complete'))

    def test_activation_expired(self):
        """
        An expired account can't be activated.

        """
        resp = self.client.post(reverse('registration_register'),
                                data={'username': 'bob',
                                      'email': 'bob@example.com',
                                      'password1': 'secret',
                                      'password2': 'secret'})

        profile = self.account_verification.objects.get(user__username='bob')
        user = profile.user
        user.date_joined -= datetime.timedelta(
            days=settings.ACCOUNT_ACTIVATION_DAYS)
        user.save()

        resp = self.client.get(
            reverse('registration_activate',
                    args=(),
                    kwargs={'activation_key': profile.activation_key}))

        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'registration/activate.html')
        user = CustomUser().objects.get(username='bob')
        self.assertFalse(user.is_active)