from django.utils.translation import ugettext_lazy as _
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class CustomJWTAuthentication(JWTAuthentication):
    def get_header(self, request):
        """
        Extracts the header containing the JSON web token from the given
        request.
        """

        header = request.META.get("HTTP_USER_KEY")

        if not header:
            raise AuthenticationFailed(
                _("Authorization header must contain USER-KEY header param"),
                code="bad_authorization_header",
            )

        if isinstance(header, str):
            # Work around django test client oddness
            header = header.encode(HTTP_HEADER_ENCODING)

        return header
