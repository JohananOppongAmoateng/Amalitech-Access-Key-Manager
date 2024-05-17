
from django.test import TestCase, Client
from django.urls import reverse
from registration.models import CustomUser
from .models import AccessKey
from .forms import CreateAccessKeyForm

class AccessKeyViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='testuser@example.com', password='testpassword')
        self.access_key = AccessKey.objects.create(user=self.user)
        
    def test_home_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, '/accounts/login/?next=/')

    def test_home_view_logged_in(self):
        self.client.login(email='testuser@example.com', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accesskey/home.html')
        self.assertIn('keys', response.context)
        self.assertQuerysetEqual(response.context['keys'], [self.access_key])

    def test_create_access_key_view_get(self):
        self.client.login(email='testuser@example.com', password='testpassword')
        response = self.client.get(reverse('create_access_key'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accesskey/create_access_key.html')
        self.assertIsInstance(response.context['form'], CreateAccessKeyForm)
        
    def test_create_access_key_view_post_invalid_form(self):
        self.client.login(email='testuser@example.com', password='testpassword')
        response = self.client.post(reverse('create_access_key'), {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accesskey/create_access_key.html')
        self.assertIsInstance(response.context['form'], CreateAccessKeyForm)
        self.assertFalse(response.context['form'].is_valid())
        
    def test_create_access_key_view_post_valid_form_with_active_key(self):
        self.client.login(email='testuser@example.com', password='testpassword')
        form_data = {'name': 'newkey'}
        response = self.client.post(reverse('create_access_key'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accesskey/home.html')
        self.assertContains(response, "You already have an active key. You cannot create a new access key")
        
    def test_create_access_key_view_post_valid_form_without_active_key(self):
        AccessKey.objects.filter(user=self.user).delete()  # Ensure there are no active keys for the user
        self.client.login(email='testuser@example.com', password='testpassword')
        form_data = {'name': 'newkey'}
        response = self.client.post(reverse('create_access_key'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accesskey/home.html')
        self.assertContains(response, "Access key created successfully")
        self.assertTrue(AccessKey.objects.filter(user=self.user, name='newkey').exists())
        

