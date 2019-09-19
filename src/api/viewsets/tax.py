import logging

from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.models import Tax
from api.serializers import TaxSerializer
from api import errors

logger = logging.getLogger(__name__)


class GetAllTaxes(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = Tax.objects.all()
        serializer = TaxSerializer(queryset, many=True)
        return Response(serializer.data)


class GetSingleTax(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, tax_id):
        try:
            tax = Tax.objects.get(tax_id=tax_id)
            serializer = TaxSerializer(instance=tax)
            return Response(serializer.data)
        except Tax.DoesNotExist:
            return errors.handle(errors.TAX_01)