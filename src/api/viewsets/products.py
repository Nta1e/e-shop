import logging

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.response import Response

from api import errors
from api.models import Category, Product, Review, ProductCategory
from api.serializers import ProductSerializer, ReviewSerializer, SingleProductSerializer
from api.pagination import StandardResultsPagination
logger = logging.getLogger(__name__)


class RetrieveProducts(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsPagination

    def get(self, request):

        products = Product.objects.all()
        paginated_data = self.paginate_queryset(products)
        products_list = list()
        for product in paginated_data:
            serializer_element = ProductSerializer(instance=product)
            products_list.append(serializer_element.data)
        return self.get_paginated_response(products_list)


class ProductsFilterClass(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='exact')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')


class SearchProducts(generics.ListAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = StandardResultsPagination

    filter_class = ProductsFilterClass
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name', 'description')


class GetSingleProduct(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SingleProductSerializer
    authentication_classes = ()

    def get(self, request, product_id):
        try:
            product = Product.objects.get(product_id=product_id)
            serializer_element = SingleProductSerializer(instance=product)
            data = self.truncate_description(request, serializer_element.data)
            return Response(data)
        except Product.DoesNotExist:
            return errors.handle(errors.PRO_01)

    def truncate_description(self, request, data):
        description_length = request.data.get('product_id', None)
        if not description_length:
            description_length = 200
        description = {
            "description": data['description'][:description_length] + '...'
        }
        _data = data
        _data.update(description)
        return _data


class GetProductsInCategory(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsPagination

    def get(self, request, category_id):
        categories = ProductCategory.objects.filter(category_id=category_id)
        if not categories:
            return errors.handle(errors.CAT_01)
        _products_list = list()
        for category in categories:
            product = Product.objects.get(product_id=category.product_id)
            _products_list.append(product)
        paginated_data = self.paginate_queryset(_products_list)
        products_list = list()
        for product in paginated_data:
            serializer_element = ProductSerializer(instance=product)
            products_list.append(serializer_element.data)
        return self.get_paginated_response(products_list)


class GetProductsInDepartment(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsPagination

    def get(self, request, department_id):
        _categories = Category.objects.filter(department_id=department_id)
        if not _categories:
            errors.handle(errors.DEP_02)

        _products_list = list()
        for category in _categories:
            prod_category = ProductCategory.objects.filter(category_id=category.category_id)
            for item in prod_category:
                product = Product.objects.get(product_id=item.product_id)
                _products_list.append(product)
        paginated_data = self.paginate_queryset(_products_list)
        products_list = list()
        for product in paginated_data:
            serializer_element = ProductSerializer(instance=product)
            products_list.append(serializer_element.data)
        return self.get_paginated_response(products_list)


class PostProductReview(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReviewSerializer

    def post(self, request):
        try:
            product_id = request.data.get('product_id', None)
            product = Product.objects.get(product_id=product_id)
            customer_id = request.user.customer_id
            review = Review()
            for field, value in request.data.items():
                setattr(review, field, value)
            customer_review = Review.objects.filter(customer_id=customer_id, product_id=product_id)
            if customer_review:
                return errors.handle(errors.USR_11)
            review.customer_id = customer_id
            review.save()
            serializer_element = ReviewSerializer(instance=review)
            holding_dict = serializer_element.data
            return_dict = {
                "name": product.name,
                **holding_dict
            }
            return Response(return_dict, 201)
        except Product.DoesNotExist:
            return errors.handle(errors.PRO_01)


class GetProductReviews(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReviewSerializer

    def get(self, request, product_id):
        try:
            product = Product.objects.get(product_id=product_id)
            review = Review.objects.get(product_id=product_id)
            serializer_element = ReviewSerializer(instance=review)
            holding_dict = serializer_element.data
            return_dict = {
                "name": product.name,
                **holding_dict
            }
            return Response(return_dict, 201)
        except Product.DoesNotExist:
            return errors.handle(errors.PRO_01)