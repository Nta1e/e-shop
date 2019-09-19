from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.payments import create, create_webhook


class StripePayment(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        test_token = "tok_1FKU4ECHn72Ds0uhBbxsduBW"
        create_webhook()
        response = create(
            amount=request.data.get('amount'),
            order_id=request.data.get('order_id'),
            currency=request.data.get('currency'),
            source=request.data.get('stripeToken', test_token),
            description=request.data.get('description')
        )
        return_data = {
            **response,
            "message": "Payment processed successfully!"
        }
        return Response(return_data)
