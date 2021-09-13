from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings

from wallet.serializers import VerifyPaymentSerializer, InitiatePaymentSerializer
from wallet.models import Payment, Wallet


@api_view(['POST'])
def initiate_payment(request):
    serializer = InitiatePaymentSerializer

    public_key = settings.PAYSTACK_PUBLIC_KEY
    received_data = request.data
    serialied_data = serializer(data=received_data)
    serialied_data.is_valid(raise_exception=True)

    course = serialied_data.data["course_to_enroll"]
    print(serialied_data.data)
    print(course.price)

    # payment_instance = Payment.objects.create(course_to_enroll)

    return Response({"n": "none"})


@api_view(['POST'])
def verify_payment(request):
    received_data = request.data
    serialied_data = VerifyPaymentSerializer(data=received_data)
    serialied_data.is_valid(raise_exception=True)


# initiate payment
# verify payment
# checkout wallet
