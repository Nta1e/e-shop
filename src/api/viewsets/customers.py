import logging

from django.contrib.auth.models import AnonymousUser
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from api.utils.facebook_validation import FacebookValidation
from api.utils.helpers import decode_token_from_request, validate_credit_card
from api import errors, serializers
from api.models import Customer
from api.serializers import CustomerSerializer, SocialSerializer

logger = logging.getLogger(__name__)


class GetCustomer(generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerSerializer

    def get(self, request):
        """
        Get a customer by ID. The customer is getting by token
        """
        customer_id = decode_token_from_request(request)
        if isinstance(request.user, AnonymousUser):
            logger.error(errors.USR_10.message)
            return errors.handle(errors.USR_10)
        customer = Customer.objects.get(customer_id=customer_id)
        serializer_element = CustomerSerializer(customer)
        return Response(serializer_element.data)


class UpdateCustomer(generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerSerializer

    def put(self, request):
        customer = request.user

        for field, value in request.data.items():
            setattr(customer, field, value)

        customer.save()
        serializer_element = CustomerSerializer(instance=customer)
        return Response(serializer_element.data, status.HTTP_200_OK)


class UpdateAddress(generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerSerializer

    def put(self, request):
        customer = request.user
        shipping_id = request.data.get("shipping_region_id", None)

        if shipping_id is None:
            errors.COM_01.message = "The field shipping_region_id is required"
            return errors.handle(errors.COM_01)

        if not isinstance(shipping_id, int):
            return errors.handle(errors.USR_09)
        for field, value in request.data.items():
            setattr(customer, field, value)

        customer.save()
        serializer_element = CustomerSerializer(instance=customer)
        return Response(serializer_element.data, status.HTTP_200_OK)


class UpdateCreditCard(generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerSerializer

    def put(self, request):

        if "credit_card" in request.data:
            credit_card = request.data.get("credit_card")
            if not validate_credit_card(credit_card):
                return errors.handle(errors.USR_08)
            customer = request.user
            customer.credit_card = credit_card
            customer.save()
            last_digits = credit_card.split("-")[-1]
            serializer_element = CustomerSerializer(customer)
            credit_field = {"credit_card": "xxxxxxxxxxxx" + str(last_digits)}
            return_dict = dict()
            return_dict.update(serializer_element.data)
            return_dict.update(credit_field)
            return Response(return_dict)

        else:
            errors.COM_01.message = "The field credit_card is required"
            return errors.handle(errors.COM_01)


class CreateCustomer(generics.GenericAPIView):
    serializer_class = CustomerSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        customer_details = {
            "name": request.data.get("name", None),
            "email": request.data.get("email", None),
            "password": request.data.get("password", None),
        }
        customer_instance = Customer.objects.create_customer(**customer_details)
        serializer = CustomerSerializer(instance=customer_instance)
        return Response(
            {"customer": serializer.data, "accessToken": "", "expiresIn": ""},
            status=201,
        )


class TokenObtainPairPatchedView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    serializer_class = serializers.TokenObtainPairPatchedSerializer


token_obtain_pair = TokenObtainPairPatchedView.as_view()


class SocialLoginView(generics.GenericAPIView):
    """Log in using facebook"""

    serializer_class = SocialSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = ()

    def post(self, request):
        logger.debug("Login a customer")
        """Authenticate user through the access_token"""
        serializer = SocialSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = serializer.data.get("access_token")

        user = FacebookValidation().validate_access_token(access_token)
        username = user.get("name", None)
        email = user.get("email", None)
        try:
            customer = Customer.objects.get(name=username)
        except Customer.DoesNotExist:
            customer = Customer.objects.create_customer(name=username, email=email)
        refresh = RefreshToken.for_user(customer)
        serializer_element = CustomerSerializer(customer)
        response = Response(
            {
                "customer": {"schema": serializer_element.data},
                "accessToken": "Bearer " + str(refresh.access_token),
                "expires_in": "24h",
            },
            200,
        )
        logger.debug("Success")
        return response
