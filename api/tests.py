from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from registration.models import CustomUser
from accesskey.models import AccessKey
from api.serializers import AccessKeySerializer


class AccessKeyDetailsWithEmailTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = CustomUser.objects.create_superuser(
            email="admin@example.com", password="adminpassword"
        )
        self.regular_user = CustomUser.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.access_key = AccessKey.objects.create(
            user=self.regular_user, key="testkey", status="active"
        )
        self.url = reverse(
            "active-key-detail",
            kwargs={"email": self.regular_user.email},
        )

    def test_get_access_key_details_with_email_not_admin(self):
        self.client.login(email="testuser@example.com", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_access_key_details_with_email_admin(self):
        self.client.login(email="admin@example.com", password="adminpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, AccessKeySerializer(self.access_key).data)

    def test_get_access_key_details_with_email_non_existent_user(self):
        self.client.login(email="admin@example.com", password="adminpassword")
        non_existent_user_url = reverse(
            "active-key-detail",
            kwargs={"email": "nonexistent@example.com"},
        )
        response = self.client.get(non_existent_user_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_access_key_details_with_email_no_active_key(self):
        self.client.login(email="admin@example.com", password="adminpassword")
        self.access_key.status = "inactive"
        self.access_key.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
