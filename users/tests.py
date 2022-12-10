from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate
# Create your tests here.


from .models import CustomUser


class ApiTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(
            username="Sadiq",
            email="sadiq1023@gmail.com",
            password=make_password("sadiq1023")
        )

    def test_user_list_view(self):
        response = self.client.get(reverse("users_list"))
        force_authenticate(response, user=self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertContains(response, self.user)
