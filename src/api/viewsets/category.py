from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import Category, ProductCategory
from api.serializers import CategorySerializer, ProductCategorySerializer
from api import errors


class GetCategories(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response({"rows": serializer.data})


class GetCategory(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, category_id):
        try:
            category = Category.objects.get(category_id=category_id)
            serializer_element = CategorySerializer(instance=category)
            return Response(serializer_element.data)
        except Category.DoesNotExist:
            return errors.handle(errors.CAT_01)


class GetProductCategory(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, product_id):
        try:
            prod_category = ProductCategory.objects.get(product_id=product_id)
            category = Category.objects.get(category_id=prod_category.category_id)
            serializer_element = ProductCategorySerializer(instance=category)
            return Response(serializer_element.data)
        except ProductCategory.DoesNotExist:
            return errors.handle(errors.PRO_02)


class GetDepartmentCategories(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, department_id):
        categories = Category.objects.filter(department_id=department_id)
        if not categories:
            return errors.handle(errors.CAT_02)
        serializer = CategorySerializer(categories, many=True)
        return Response({"rows": serializer.data})
