import facebook
from facebook import GraphAPIError
from rest_framework.exceptions import ValidationError


class FacebookValidation:
    @staticmethod
    def validate_access_token(access_token):
        try:
            graph = facebook.GraphAPI(access_token=access_token, version="3.1")
            user_data = graph.request("/me?fields=name,email")
            return user_data

        except GraphAPIError as error:
            raise ValidationError(
                {"error": {"access_token": "Invalid token", "details": str(error)}}
            )
