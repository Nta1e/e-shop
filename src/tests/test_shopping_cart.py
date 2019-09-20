from django.urls import reverse

from .base import BaseTestCase


class ShoppingCartTestCase(BaseTestCase):
    def test_generate_cart_id(self):
        response = self.client_with_token().get(reverse("generate_cart_id"))
        self.assertEqual(response.status_code, 201)

    def test_add_products_to_cart(self):
        response = self.client_with_token().post(
            reverse("add_products"), data=self.cart_data, format="json"
        )
        self.assertEqual(response.status_code, 201)

    def test_get_products_in_cart(self):
        response = self.client_with_token().get(
            reverse("get_products_in_cart", kwargs={"cart_id": "186963645"})
        )
        self.assertEqual(response.status_code, 200)

    def test_update_quantity(self):
        response = self.client_with_token().put(
            reverse("update_quantity", kwargs={"item_id": 1}),
            data={"quantity": 23},
            format="json",
        )
        self.assertEqual(response.status_code, 201)

    def test_empty_cart(self):
        response = self.client_with_token().delete(
            reverse("empty_cart", kwargs={"cart_id": "186963645"})
        )
        self.assertEqual(response.status_code, 200)

    def test_remove_item(self):
        response = self.client_with_token().delete(
            reverse("remove_item", kwargs={"item_id": 1})
        )
        self.assertEqual(response.status_code, 200)
