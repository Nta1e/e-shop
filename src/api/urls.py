import logging

from django.urls import path, include
from rest_framework import routers

from api.viewsets.attribute import AttributeViewSet

from api.viewsets.category import (
    GetCategories,
    GetCategory,
    GetProductCategory,
    GetDepartmentCategories
)
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
from api.viewsets.orders import (
    PlaceOrder,
    GetOrder,
    GetCustomerOrder,
    GetOrdersShortDetails
)
from api.viewsets.products import (
    RetrieveProducts,
    SearchProducts,
    GetSingleProduct,
    GetProductsInCategory,
    GetProductsInDepartment,
    PostProductReview,
    GetProductReviews
)
from api.viewsets.shipping_region import ShippingRegionViewSet
from api.viewsets.shoppingcart import (
    GenerateCartID,
    AddProducts,
    GetProducts,
    UpdateQuantity,
    EmptyCart,
    RemoveProduct,
)
from api.viewsets.stripe import charge, webhooks
from api.viewsets.tax import TaxViewSet

logger = logging.getLogger(__name__)

router = routers.DefaultRouter()
router.register(r"departments", DepartmentViewSet)

router.register(r"attributes", AttributeViewSet)
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
    path("customer", GetCustomer.as_view(), name="get_customer"),
    path("customer/update", UpdateCustomer.as_view(), name="update_details"),
    path("customers", CreateCustomer.as_view(), name="create_customer"),
    path("customers/login", token_obtain_pair, name="login_customer"),
    path("customers/facebook", SocialLoginView.as_view(), name="facebook_login"),
    path("customer/address", UpdateAddress.as_view(), name="update_address"),
    path("customer/creditCard", UpdateCreditCard.as_view(), name="update_credit_card"),
    path(
        "shoppingcart/generateUniqueId",
        GenerateCartID.as_view(),
        name="generate_cart_id",
    ),
    path("shoppingcart/add", AddProducts.as_view(), name="add_products"),
    path(
        "shoppingcart/<str:cart_id>", GetProducts.as_view(), name="get_products_in_cart"
    ),
    path(
        "shoppingcart/update/<int:item_id>",
        UpdateQuantity.as_view(),
        name="update_quantity",
    ),
    path("shoppingcart/empty/<str:cart_id>", EmptyCart.as_view(), name="empty_cart"),
    path(
        "shoppingcart/removeProduct/<int:item_id>",
        RemoveProduct.as_view(),
        name="remove_item",
    ),
    path("products", RetrieveProducts.as_view(), name="retrieve_products"),
    path("products/search", SearchProducts.as_view(), name="search_products"),
    path("products/<int:product_id>", GetSingleProduct.as_view(), name="get_product"),
    path(
        "products/inCategory/<int:category_id>",
        GetProductsInCategory.as_view(),
        name="products_in_category",
    ),
    path(
        "products/inDepartment/<int:department_id>",
        GetProductsInDepartment.as_view(),
        name="products_in_dpt",
    ),
    path("products/reviews", PostProductReview.as_view(), name="post_review"),
    path("products/<int:product_id>/reviews", GetProductReviews.as_view(), name="get_reviews"),
    path("orders", PlaceOrder.as_view(), name="place_order"),
    path("orders/<int:order_id>", GetOrder.as_view(), name="get_order"),
    path("orders/InCustomer", GetCustomerOrder.as_view(), name="customer_order"),
    path("orders/shortDetail/<int:order_id>", GetOrdersShortDetails.as_view(), name="order_detail"),
    path("categories", GetCategories.as_view(), name="get_categories"),
    path("categories/<int:category_id>", GetCategory.as_view(), name="get_category"),
    path("categories/inProduct/<int:product_id>", GetProductCategory.as_view(), name="product_category"),
    path("categories/inDepartment/<int:department_id>", GetDepartmentCategories.as_view(), name="department_categories")
]
