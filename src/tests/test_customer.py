from unittest.mock import patch
from django.urls import reverse
from .base import BaseTestCase


class CustomerTestCase(BaseTestCase):

    def test_successful_customer_registration(self):
        response = self.client.post(
            reverse("create_customer"),
            self.customer_data("Ntale", "Ntale@turing.com", "password123"),
            format="json",
        )
        self.assertEqual(response.status_code, 201)

    def test_wrong_email(self):
        response = self.client.post(
            reverse("create_customer"),
            self.customer_data("Ntale", "Ntale@gmailcom", "password123"),
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("USR_03", response.data["error"]["code"])

    def test_duplicate_email(self):
        self.client.post(
            reverse("create_customer"),
            self.customer_data("Ntale", "Ntale@gmail.com", "password123"),
            format="json",
        )
        response = self.client.post(
            reverse("create_customer"),
            self.customer_data("Ntale", "Ntale@gmail.com", "password123"),
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("USR_04", response.data["error"]["code"])

    def test_successful_customer_login(self):
        self.client.post(
            reverse("create_customer"),
            self.customer_data("Ntale", "Ntale@turing.com", "password123"),
            format="json",
        )
        response = self.client.post(
            reverse("login_customer"),
            self.login_data,
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data['accessToken'])

    def test_invalid_login_credentials(self):
        response = self.client.post(
            reverse("login_customer"),
            self.login_data,
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_facebook_login(self):
        with patch(
            "api.utils.facebook_validation.FacebookValidation.validate_access_token"
        ) as mock_facebook:
            mock_facebook.return_value = {
                "id": "1234587649",
                "name": "Ntale Shadik",
                "email": "Shadikntale@turing.com",
            }
            mock_facebook("token")
            response = self.client.post(
                reverse("facebook_login"), {"access_token": "validToken"}, format="json"
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn("accessToken", response.data)

    def test_get_customer(self):
        response = self.client_with_token().get(
            reverse("get_customer"),
            format="json",
        )
        self.assertEqual(response.status_code, 200)