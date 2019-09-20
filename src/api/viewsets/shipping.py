import logging

from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.models import ShippingRegion, Shipping
from api.serializers import ShippingRegionSerializer, ShippingSerializer
from api import errors

logger = logging.getLogger(__name__)


class GetShippingRegions(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = ShippingRegion.objects.all()
        serializer = ShippingRegionSerializer(queryset, many=True)
        return Response(serializer.data)


class GetRegionShippings(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, shipping_region_id):
        shipping = Shipping.objects.filter(shipping_region_id=shipping_region_id)
        if not shipping:
            return errors.handle(errors.SHP_02)
        serializer = ShippingSerializer(shipping, many=True)
        return Response(serializer.data)
