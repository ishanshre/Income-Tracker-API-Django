from rest_framework.test import APITestCase

from django.urls import reverse

class TestSetUp(APITestCase):
    def setUp(self):
        self.register_url = reverse('accounts:register')
        self.login_url = reverse('accounts:login')
        self.user_data = {
            'username':'world',
            'email':'test@test.com',
            'password':'hello@123',
            'password2':'hello@123'
        }
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()