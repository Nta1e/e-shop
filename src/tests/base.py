from django.core.management import call_command
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from api.models import Category, ProductCategory, Product


class BaseTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_data = {"email": "Ntale@turing.com", "password": "password123"}
        self.review_data = {
                "product_id": 1,
                "review": "good...",
                "rating": 5
        }
        self.cart_data = {
            "cart_id": "186963646",
            "product_id": 1,
            "attributes": "good",
            "quantity": 5
        }
        self.order_data = {
            "cart_id": "186963645",
            "shipping_id": 1,
            "tax_id": 1
        }
        call_command('loaddata', 'tests')

    def customer_data(self, name, email, password):
        data = {"name": name, "email": email, "password": password}
        return data

    def client_with_token(self):
        data = self.customer_data("Ntale", "Ntale@turing.com", "password123")
        res = self.client.post(reverse("create_customer"), data, format="json")
        response = self.client.post(
            reverse("login_customer"), self.login_data, format="json"
        )
        access_token = response.data["accessToken"]
        client = self.client
        client.credentials(HTTP_USER_KEY=access_token)
        return client

    @property
    def create_category(self):
        category = Category(
            department_id=1,
            name="Flower",
            description="colourful!"
        )
        category.save()
        return category
