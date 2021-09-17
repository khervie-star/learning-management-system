from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from wallet.serializers import (
    VerifyPaymentSerializer, InitiatePaymentSerializer,
    PaymentSerializer, WalletSerilaizer
)
from wallet.models import Payment, Wallet
from course.models import Course
from instructor.models import Instructor


@api_view(['POST'])
def initiate_payment(request):
    serializer = InitiatePaymentSerializer

    public_key = settings.PAYSTACK_PUBLIC_KEY
    received_data = request.data
    serialized_data = serializer(data=received_data)
    serialized_data.is_valid(raise_exception=True)

    isAuthenticated = request.user.is_authenticated
    course_slug = received_data["course_slug"]
    try:
        course = Course.objects.get(slug=course_slug)
    except ObjectDoesNotExist:
        return Response({"message": "Course with the provided slug doesn’t exist"}, "404")
    else:
        serializer = PaymentSerializer

        email = serialized_data.data["email"]
        if isAuthenticated:
            payment_instance = Payment.objects.create(
                course_to_enroll=course, email=email, auth_student=isAuthenticated, amount=course.price)
        else:
            payment_instance = Payment.objects.create(
                course_to_enroll=course, email=email, amount=course.price)

        serialized_data = serializer(payment_instance)
    return Response({"data": serialized_data.data, "public_key": public_key})


@api_view(['GET'])
def verify_payment(request):
    received_data = request.data
    serialized_data = VerifyPaymentSerializer(data=received_data)
    serialized_data.is_valid(raise_exception=True)
    try:
        payment = Payment.objects.get(reference=serialized_data["payment_reference"].value)
    except ObjectDoesNotExist:
        return Response({"message": "Payment instance does not exist"})
    else:
        payment.transaction_ref = serialized_data["transaction_reference"].value
        payment.save()
        verify_payment, message = payment.verify_payment()

        # verify the payment
        if verify_payment:
            # update instructor wallet on successfully payment
            instructor = Instructor.objects.get(Instructor=payment.course_to_enroll.author)

            wallet = wallet.objects.get(wallet_owner=instructor)
            wallet.balance += payment.course_to_enroll.price
            wallet.save()

            return Response({"status": True, "message": "Payment successfully"}, status="200")
        else:
            return Response({"status": False, "message": message}, status="200")


@api_view(['GET'])
def my_wallet(request):
    """
    only an instance of an instructor should call this endpoint
    """

    serializer = WalletSerilaizer
    authenticated_user = request.user
    try:
        instructor = Instructor.objects.get(instructor=authenticated_user)
    except ObjectDoesNotExist:
        return Response({"message": "Access Denied. You are not an instructor"}, status="403")
    else:
        wallet = Wallet.objects.get(wallet_owner=instructor)
        serialized_data = serializer(wallet)
        return Response({"data": serialized_data.data}, status="200")


"""
Get transaction details
"""
