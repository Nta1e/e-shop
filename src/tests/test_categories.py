from django.urls import reverse

from .base import BaseTestCase


class CategoriesTestCase(BaseTestCase):

    def test_get_categories(self):
        response = self.client_with_token().get(
            reverse('get_categories')
        )
        self.assertEqual(response.status_code, 200)

    def test_get_category(self):
        response = self.client_with_token().get(
            reverse("get_category",
                    kwargs={
                        "category_id": 1
                    })
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_in_category(self):
        response = self.client_with_token().get(
            reverse('product_category',
                    kwargs={
                        "product_id": 1
                    })
        )
        self.assertEqual(response.status_code, 200)
