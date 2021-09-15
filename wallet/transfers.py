from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model

from wallet.models import Transfers, Wallet
from instructor.models import Instructor
from wallet.paystack import PayStack as PS

# Create Transfer Receipent
# ensure the money they want to transfer is actually in their wallet

# just for testing purpose now
User = get_user_model().objects.all()[0]


@api_view(['POST'])
def verify_account_number(request, *args, **kwargs):
    # Only instances of an Instructor should be allowed
    """
    A form should be displayed to the user at the frontend
    a request should be made at the frontend to "https://api.paystack.co/bank"
    then should send the users:
    --> account_number,
    --> bank_code,
    --> currency,
    --> bank_type e.g "nuban"
    --> bank_name
    --> amount
    """
    # authenticated_user = request.user
    # change this line
    authenticated_user = User
    received_data = request.data
    # serializer all of this
    account_number = received_data["account_number"]
    bank_code = received_data["bank_code"]
    currency = received_data["currency"]
    bank_type = received_data["bank_type"]
    bank_name = received_data["bank_name"]
    amount = received_data["amount"]

    try:
        wallet_instance = Wallet.objects.get(instructor=authenticated_user)
    except ObjectDoesNotExist:
        return Response({"status": False, "message": "You are not authorized to access this endpoint"})
    else:
        #  verify the amount to be checked out is >= to wallet balance
        if wallet_instance.balance < amount:
            return Response({"status": "False", "message": "Insufficient Balance"})

    # resolve account
    status, is_account_valid = PS.resolve_account_number(account_number, bank_code)

    if not status:
        return Response(is_account_valid)

    data = is_account_valid["data"]
    # create transfer instance
    transfer_instance = Transfers.objects.create(
        instructor=authenticated_user, account_number=data["account_number"],
        account_name=data["account_name"], bank_code=bank_code, currency=currency,
        bank_name=bank_name, bank_type=bank_type, amount=amount
    )

    # create transfer receipent
    params = {
        "bank_type": transfer_instance.bank_type,
        "name": transfer_instance.account_name,
        "account_number": transfer_instance.account_number,
        "bank_code": transfer_instance.bank_code,
        "currency": transfer_instance.currency
    }

    status, transfer_recipient = PS.transfer_recipient(**params)

    if not status:
        return Response(transfer_recipient)

    data = transfer_recipient["data"]

    transfer_instance.recipient_code = data["recipient"]

    transfer_instance.save()

    # initiate payment
    status, initiate_transfer_resp = PS.initiate_payment(
        transfer_instance.amount, transfer_instance.recipient_code)

    if not status:
        return Response(initiate_transfer_resp)

    data = initiate_transfer_resp["data"]
    transfer_instance.transfer_reference(data["reference"])
    transfer_instance.save()

    # deduct wallet balance on successfully transfer
    return Response({}, status="200")


@api_view(['POST'])
def transfer_status_webhook(*args, **kwargs):
    event = request.body

    return Response(status="200")
