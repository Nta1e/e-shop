from rest_framework.test import APITestCase, APIClient


class BaseTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.customer = {
            "name": "Ntale Shadik",
            "email": "shadik@gmail.com",
            "password": "password123"
        }
