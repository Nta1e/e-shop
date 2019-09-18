import logging

from django.urls import path, include
from rest_framework import routers

from api.viewsets.attribute import AttributeViewSet

# from api.viewsets.category import CategoryViewSet
# TODO: Implement category
from api.viewsets.customers import (
    CreateCustomer,
    token_obtain_pair,
    SocialLoginView,
    UpdateAddress,
    UpdateCreditCard,
    GetCustomer,
    UpdateCustomer,
)
from api.viewsets.department import DepartmentViewSet
from api.viewsets.orders import create_order, order, orders, order_details
from api.viewsets.products import ProductViewSet
from api.viewsets.shipping_region import ShippingRegionViewSet
from api.viewsets.shoppingcart import (
    GenerateCartID,
    AddProducts,
    GetProducts,
    UpdateQuantity,
    EmptyCart,
    RemoveProduct
)
from api.viewsets.stripe import charge, webhooks
from api.viewsets.tax import TaxViewSet

logger = logging.getLogger(__name__)

router = routers.DefaultRouter()
router.register(r"departments", DepartmentViewSet)

router.register(r"attributes", AttributeViewSet)
router.register(r"products", ProductViewSet)
router.register(r"tax", TaxViewSet)
router.register(r"shipping/regions", ShippingRegionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "attributes/values/<int:attribute_id>/",
        AttributeViewSet.as_view({"get": "get_values_from_attribute"}),
    ),
    path(
        "attributes/inProduct/<int:product_id>/",
        AttributeViewSet.as_view({"get": "get_attributes_from_product"}),
    ),
    path(
        "products/inCategory/<int:category_id>",
        ProductViewSet.as_view({"get": "get_products_by_category"}),
    ),
    path(
        "products/inDepartment/<int:department_id>",
        ProductViewSet.as_view({"get": "get_products_by_department"}),
    ),
    path("customer", GetCustomer.as_view(), name="get_customer"),
    path("customer/update", UpdateCustomer.as_view(), name="update_details"),
    path("customers", CreateCustomer.as_view(), name="create_customer"),
    path("customers/login", token_obtain_pair, name="login_customer"),
    path("customers/facebook", SocialLoginView.as_view(), name="facebook_login"),
    path("customer/address", UpdateAddress.as_view(), name="update_address"),
    path("customer/creditCard", UpdateCreditCard.as_view(), name="update_credit_card"),
    path("shoppingcart/generateUniqueId", GenerateCartID.as_view(), name="generate_cart_id"),
    path("shoppingcart/add", AddProducts.as_view(), name="add_products"),
    path("shoppingcart/<str:cart_id>", GetProducts.as_view(), name="get_products_in_cart"),
    path("shoppingcart/update/<int:item_id>", UpdateQuantity.as_view(), name="update_quantity"),
    path("shoppingcart/empty/<str:cart_id>", EmptyCart.as_view(), name="empty_cart"),
    path("shoppingcart/removeProduct/<int:item_id>", RemoveProduct.as_view(), name="remove_item")

]
