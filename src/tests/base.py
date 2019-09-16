from django.urls import reverse
from rest_framework.test import APITestCase, APIClient


class BaseTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_data = {
            "email": "Ntale@turing.com",
            "password": "password123"
        }

    def customer_data(self, name, email, password):
        data = {"name": name, "email": email, "password": password}
        return data

    def client_with_token(self):
        data = self.customer_data("Ntale", "Ntale@turing.com", "password123")
        res = self.client.post(reverse('create_customer'), data, format='json')
        response = self.client.post(reverse('login_customer'), self.login_data, format='json')
        access_token = response.data['accessToken']
        client = self.client
        client.credentials(HTTP_USER_KEY=access_token)
        return client
