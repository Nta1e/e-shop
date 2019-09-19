import logging

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api import errors
from api.models import (
    Orders,
    Shipping,
    Tax,
    ShoppingCart,
    Product
)
from api.utils.mail import SendMail

logger = logging.getLogger(__name__)


class PlaceOrder(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        shipping_id = request.data.get("shipping_id", None)
        tax_id = request.data.get("tax_id", None)
        cart_id = request.data.get("cart_id", None)
        try:
            Shipping.objects.get(shipping_id=shipping_id)
            Tax.objects.get(tax_id=tax_id)
            carts = ShoppingCart.objects.filter(cart_id=cart_id)
            if not carts:
                return errors.handle(errors.CRT_01)
            placed_order = Orders.objects.filter(reference=cart_id)
            if placed_order:
                return errors.handle(errors.ORD_03)
            order = Orders()
            for field, value in request.data.items():
                setattr(order, field, value)
            order.customer_id = request.user.customer_id
            order.reference = cart_id
            order.save()
            subject = "Order Received!"
            to_email = [request.user.email]
            context = {
                "username": request.user.name,
                "reference": order.reference,
                "order_id": order.order_id
            }
            mail = SendMail('notify_order.html', context, subject, to_email)
            mail.send()
            return_dict = {"order_id": order.order_id}
            return Response(return_dict, 201)

        except Shipping.DoesNotExist:
            return errors.handle(errors.SHP_01)

        except Tax.DoesNotExist:
            return errors.handle(errors.TAX_01)


class GetOrder(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, order_id):
        try:
            order = Orders.objects.get(order_id=order_id)
            cart_items = ShoppingCart.objects.filter(cart_id=order.reference)
            _product_list = list()
            for item in cart_items:
                product = Product.objects.get(product_id=item.product_id)
                holding_dict = {
                    "product_id": product.product_id,
                    "attributes": item.attributes,
                    "product_name": product.name,
                    "quantity": item.quantity,
                    "unit_cost": product.price/item.quantity,
                    "sub_total": product.price*item.quantity
                }
                _product_list.append(holding_dict)
            return_dict = {
                "order_id": order_id,
                "order_items": _product_list
            }
            return Response(return_dict)
        except Orders.DoesNotExist:
            return errors.handle(errors.ORD_01)


class GetCustomerOrder(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        customer_id = request.user.customer_id
        orders = Orders.objects.filter(customer_id=customer_id)
        orders_list = list()
        for order in orders:
            holding_dict = {
                "order_id": order.order_id,
                "total_amount": order.total_amount,
                "created_on": order.created_on,
                "shipped_on": order.shipped_on,
                "name": request.user.name
            }
            orders_list.append(holding_dict)
        return Response(orders_list)


class GetOrdersShortDetails(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, order_id):
        try:
            order = Orders.objects.get(order_id=order_id)
            cart_items = ShoppingCart.objects.filter(cart_id=order.reference)
            details_list = list()
            for item in cart_items:
                product = Product.objects.get(product_id=item.product_id)
                details_dict = {
                    "order_id": order.order_id,
                    "total_amount": str(order.total_amount),
                    "created_on": order.created_on,
                    "shipped_on": order.shipped_on if order.shipped_on is not None else '',
                    "status": order.status,
                    "name": product.name
                }
                details_list.append(details_dict)
            return Response(details_list)
        except Orders.DoesNotExist:
            return errors.handle(errors.ORD_01)
