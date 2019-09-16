from django.urls import reverse
from .base import BaseTestCase

class CustomerTestCase(BaseTestCase):

    def test_successful_customer_registration(self):
        response = self.client.post(reverse('create_customer'), self.customer, format='json')
        self.assertEqual(response.status_code, 201)
