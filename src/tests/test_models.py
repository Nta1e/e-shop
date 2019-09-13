from django.test import TestCase
from api.models import Attribute


class ModelsTestCase(TestCase):

    def test_category_model(self):
        category = Attribute(
            attribute_id=1,
            name='new!'
        )
        self.assertEqual(str(category), 'new!')
