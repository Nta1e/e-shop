import random

from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from api import errors
from api.models import ShoppingCart, Product
from api.serializers import ShoppingcartSerializer
import logging

logger = logging.getLogger(__name__)


class GenerateCartID(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        """
        Generate the unique CART ID
        """
        cart_id = random.randint(100000000, 999999999)
        logger.debug("Generating cart ID")
        return Response({"cart_id": str(cart_id)}, 201)


class AddProducts(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = ShoppingcartSerializer

    def post(self, request):

        cart_id = request.data.get("cart_id")
        shopping_cart = ShoppingCart.objects.filter(cart_id=cart_id)
        product_id = request.data.get("product_id", None)
        if len(shopping_cart) > 0:
            for cart_instance in shopping_cart:
                if cart_instance.product_id == product_id:
                    return errors.handle(errors.CRT_02)

        cart = ShoppingCart()
        for field, value in request.data.items():
            setattr(cart, field, value)

        cart.save()
        serializer_element = ShoppingcartSerializer(instance=cart)
        cart_id_field = {"cart_id": int(request.data.get("cart_id"))}
        new_dict = serializer_element.data
        new_dict.update(cart_id_field)
        return Response(new_dict, 201)


class GetProducts(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, cart_id):

        cart: ShoppingCart = ShoppingCart.objects.filter(cart_id=cart_id)
        if not cart:
            return errors.handle(errors.CRT_01)

        cart_items = []
        for product in cart:
            pdt: Product = Product.objects.get(product_id=product.product_id)
            _product = {
                "item_id": product.item_id,
                "cart_id": int(product.cart_id),
                "name": pdt.name,
                "attributes": product.attributes,
                "product_id": product.product_id,
                "image": pdt.image,
                "price": str(pdt.price),
                "discounted_price": str(pdt.discounted_price),
                "quantity": product.quantity,
                "subtotal": pdt.price * product.quantity,
            }
            cart_items.append(_product)
        return Response(cart_items, 200)


class UpdateQuantity(generics.GenericAPIView):
    def put(self, request, item_id):
        try:
            cart_item = ShoppingCart.objects.get(item_id=item_id)
            quantity = request.data.get("quantity", None)
            if not quantity:
                return errors.handle(errors.COM_02)
            cart_item.quantity = request.data.get("quantity", None)
            cart_item.save()
            serializer_element = ShoppingcartSerializer(instance=cart_item)
            cart_id_field = {"cart_id": int(cart_item.cart_id)}
            new_dict = serializer_element.data
            new_dict.update(cart_id_field)
            return Response(new_dict, 201)
        except ShoppingCart.DoesNotExist:
            return errors.handle(errors.CRT_03)


class EmptyCart(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, cart_id):
        cart = ShoppingCart.objects.filter(cart_id=cart_id)
        if not cart:
            return errors.handle(errors.CRT_01)
        for item in cart:
            item.delete()
        return Response([], 200)


class RemoveProduct(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, item_id):
        try:
            item = ShoppingCart.objects.get(item_id=item_id)
            item.delete()
            return Response({"message": "Item successfully removed from cart!"})
        except ShoppingCart.DoesNotExist:
            return errors.handle(errors.CRT_03)
