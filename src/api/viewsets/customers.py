import logging
import re
from itertools import groupby

from django.contrib.auth import login
from django.contrib.auth.models import AnonymousUser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden
from social_django.utils import load_strategy, load_backend

from api.utils.facebook_validation import FacebookValidation
from api import errors, serializers
from api.models import Customer
from api.serializers import CustomerSerializer, UserSerializer, UpdateCustomerSerializer, \
    SocialSerializer, CustomerAddressSerializer

logger = logging.getLogger(__name__)


@api_view(['GET'])
def customer(request):
    """
    Get a customer by ID. The customer is getting by token
    """
    logger.debug("Getting customer")
    user = request.user
    if isinstance(user, AnonymousUser):
        logger.error(errors.USR_10.message)
        return errors.handle(errors.USR_10)
    serializer_element = CustomerSerializer(user.customer)
    logger.debug("Success")
    return Response(serializer_element.data)


@swagger_auto_schema(method="PUT", request_body=UpdateCustomerSerializer)
@api_view(['PUT'])
def update_customer(request):
    """    
    Update a customer
    """
    logger.debug("Updating customer")
    # TODO: place the code here


class CreateCustomer(generics.GenericAPIView):
    serializer_class = CustomerSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        customer_details = {
            "name": request.data.get("name", None),
            "email": request.data.get("email", None),
            "password": request.data.get("password", None)
        }
        customer_instance = Customer.objects.create_customer(**customer_details)
        serializer = CustomerSerializer(instance=customer_instance)

        return Response({"customer": serializer.data,
                         "accessToken": "",
                         "expiresIn": ""
                         }, status=201)


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

    def post(self, request):
        logger.debug("Login a customer")
        """Authenticate user through the access_token"""
        serializer = SocialSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = serializer.data.get('access_token')

        user = FacebookValidation().validate_access_token(access_token)
        username = user.get('name', None)
        email = user.get('email', None)
        try:
            customer = Customer.objects.get(name=username)
        except Customer.DoesNotExist:
            customer = Customer.objects.create_customer(name=username,
                                                    email=email)
        refresh = RefreshToken.for_user(customer)
        serializer_element = CustomerSerializer(customer)
        response = Response({
            'customer': {
                'schema': serializer_element.data
            },
            'accessToken': 'Bearer ' + str(refresh.access_token),
            'expires_in': '24h'
        }, 200)
        logger.debug("Success")
        return response


@permission_classes((IsAuthenticated,))
@swagger_auto_schema(method="PUT", request_body=CustomerAddressSerializer)
@api_view(['PUT'])
def update_address(request):
    """    
    Update the address from customer
    """
    # TODO: place the code here


def count_consecutive(num):
    return max(len(list(g)) for _, g in groupby(num))


def validate_credit_card(num):
    logger.debug("Validating credit card")
    pattern = re.compile(r'(?:\d{4}-){3}\d{4}|\d{16}')

    if not pattern.fullmatch(num) or count_consecutive(num.replace('-', '')) >= 4:
        return False
    else:
        return True


@swagger_auto_schema(method='PUT', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'credit_card': openapi.Schema(type=openapi.TYPE_STRING, description='Credit Card.', required=['true']),
    }
))
@api_view(['PUT'])
def update_credit_card(request):
    """    
    Update the credit card from customer
    """
    logger.debug("Updating credit card")
    if 'credit_card' in request.data:

        if not validate_credit_card(request.data.get('credit_card')):
            logger.error(errors.USR_08.message)
            return errors.handle(errors.USR_08)

        try:
            customer = request.user.customer
            customer.credit_card = request.data.get('credit_card', None)
            customer.save()
            serializer_element = CustomerSerializer(customer)
            logger.debug("Success")
            return Response(serializer_element.data)
        except AttributeError:
            logger.error(errors.USR_10.message)
            return errors.handle(errors.USR_10)
        except Exception as error:
            errors.COM_02.message = str(error)
            logger.error(errors.COM_02.message)
            return errors.handle(errors.COM_02)
    else:
        errors.COM_02.field = 'credit_card'
        logger.error(errors.COM_02.message)
        return errors.handle(errors.COM_02)
