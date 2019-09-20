import logging

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api import errors
from api.models import Attribute, AttributeValue, ProductAttribute
from api.serializers import (
    AttributeSerializer,
    AttributeValueSerializer,
    AttributeValueExtendedSerializer,
)

logger = logging.getLogger(__name__)


class GetAttributes(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = Attribute.objects.all()
        serializer = AttributeSerializer(queryset, many=True)
        return Response(serializer.data)


class GetSingleAttribute(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, attribute_id):
        try:
            attribute = Attribute.objects.get(attribute_id=attribute_id)
            serializer_element = AttributeSerializer(instance=attribute)
            return Response(serializer_element.data)
        except Attribute.DoesNotExist:
            return errors.handle(errors.ATR_01)


class GetAttributeValues(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, attribute_id):
        try:
            queryset = AttributeValue.objects.filter(attribute_id=attribute_id)
            serializer = AttributeValueSerializer(queryset, many=True)
            return Response(serializer.data)
        except AttributeValue.DoesNotExist:
            return errors.handle(errors.ATR_02)


class GetProductAttributes(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, product_id):
        product_attrs = ProductAttribute.objects.filter(product_id=product_id)
        return_data = list()
        for item in product_attrs:
            attribute_value = AttributeValue.objects.get(
                attribute_value_id=item.attribute_value_id
            )
            attribute = Attribute.objects.get(attribute_id=attribute_value.attribute_id)
            serializer = AttributeValueExtendedSerializer(attribute_value)
            _return_dict = {"attribute_name": attribute.name, **serializer.data}
            return_data.append(_return_dict)
        return Response(return_data)
