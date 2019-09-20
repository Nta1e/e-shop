from django.urls import reverse

from .base import BaseTestCase


class OrdersTestCase(BaseTestCase):
    def test_create_order(self):
        response = self.client_with_token().post(
            reverse("place_order"), data=self.order_data, format="json"
        )
        self.assertEqual(response.status_code, 201)

    def test_get_single_order(self):
        _response = self.client_with_token().post(
            reverse("place_order"), data=self.order_data, format="json"
        )
        response = self.client_with_token().get(
            reverse("get_order", kwargs={"order_id": _response.data.get("order_id")})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_customer_order(self):
        response = self.client_with_token().get(reverse("customer_order"))
        self.assertEqual(response.status_code, 200)

    def test_short_order_detail(self):
        _response = self.client_with_token().post(
            reverse("place_order"), data=self.order_data, format="json"
        )
        response = self.client_with_token().get(
            reverse("order_detail", kwargs={"order_id": _response.data.get("order_id")})
        )
        self.assertEqual(response.status_code, 200)
