from django.urls import reverse
from .base import BaseTestCase


class ProductsTestCase(BaseTestCase):
    def test_retrieve_products(self):
        response = self.client.get(reverse("retrieve_products"), format="json")
        self.assertEqual(response.status_code, 200)

    def test_get_products_in_category(self):
        response = self.client.get(
            reverse("products_in_category", kwargs={"category_id": 1})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_single_product(self):
        response = self.client.get(reverse("get_product", kwargs={"product_id": 1}))
        self.assertEqual(response.status_code, 200)

    def test_get_products_in_department(self):
        response = self.client.get(
            reverse("products_in_dpt", kwargs={"department_id": 1})
        )
        self.assertEqual(response.status_code, 200)

    def test_post_product_reviews(self):
        response = self.client_with_token().post(
            reverse("post_review"), data=self.review_data, format="json"
        )
        self.assertEqual(response.status_code, 201)
