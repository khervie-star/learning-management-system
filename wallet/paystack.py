import requests
import json
from django.conf import settings


class PayStack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    BASE_URL = 'https://api.paystack.co'

    def verify_payment(self, ref, *args, **kwargs):
        """
        used to verify payment success or failure.
        """
        verify_payment_endpoint = f'/transaction/verify/{ref}'
        headers = {
            'Authorization':  f'Bearer {PayStack().PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json'
        }
        path = PayStack().BASE_URL + verify_payment_endpoint
        response = requests.get(path, headers=headers)

        data = response.json()
        if response.status_code == 200:
            return data['status'], data['data']
        else:
            return data['status'], data['message']

    @staticmethod
    def resolve_account_number(account_number: int, bank_code: int) -> dict:
        """
        Verifies a given account number
        """
        resolve_account_number_endpoint = f"/bank/resolve?account_number={account_number}&bank_code={bank_code}"
        method = 'GET'
        headers = {
            'Authorization':  f'Bearer {PayStack().PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json'
        }

        path = PayStack().BASE_URL + resolve_account_number_endpoint

        _request = requests.get(path, headers=headers)

        if _request.status_code == 200:
            # -> {status, msg, data:{account_number, account_name, bank_id}}
            return True, _request.json()
        else:
            return False, _request.json()
