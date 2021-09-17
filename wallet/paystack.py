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

        if not _request.status_code == 200:
            return False, _request.json()
        else:
            # -> {status, msg, data:{account_number, account_name, bank_id}}
            return True, _request.json()

    @staticmethod
    def bank_list():
        """
        Lists the available PayStack's banks details i.e bank_code
        """
        bank_list_endpoint = "/bank"
        path = PayStack().BASE_URL + bank_list_endpoint
        mathod = 'GET'
        headers = {
            'Authorization':  f'Bearer {PayStack().PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json'
        }

        _request = requests.get(path, headers=headers)

        if not _request.status_code == 200:
            return False, _request.json()
        else:
            # -> {status, msg, data:{name, slug, code, type, currency}}
            return True, _request.json()

    @staticmethod
    def transfer_recipient(bank_type: str, name: str, account_number: int, bank_code: int, currency: str) -> dict:
        # name is account name
        transfer_recipient_endpoint = '/transferrecipient'
        method = 'POST'
        headers = {
            'Authorization':  f'Bearer {PayStack().PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json'
        }

        params = {
            "type": bank_type,
            "name": name,
            "account_number": account_number,
            "bank_code": bank_code,
            "currency": currency
        }

        params = json.dumps(params)

        path = PayStack().BASE_URL + transfer_recipient_endpoint

        _request = requests.post(path, data=params, headers=headers)

        if not _request.status_code >= 200 and _request.status_code <= 300:
            return False, _request.json()
        else:
            return True, _request.json()  # -> {status, msg, data: {recipient_code}}

    @staticmethod
    def initiate_transfer(amount, recipient_code):
        """
        This makes the actual transfer
        """
        transfer_endpoint = '/transfer'
        headers = {
            'Authorization':  f'Bearer {PayStack().PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json'
        }

        path = PayStack().BASE_URL + transfer_endpoint

        method = 'POST'

        params = {
            "source": "balance",
            "amount": amount,
            "recipient": recipient_code,
            "reason": "checkout Wallet"
        }

        params = json.dumps(params)

        _request = requests.post(path, data=params, headers=headers)

        if not _request.status_code >= 200 and _request.status_code <= 300:
            return False, _request.json()
        else:
            return True, _request.json()  # -> {status, msg, data: {reference}}

    def fetch_transfer():
        pass


# how to retry transfers
# listen for transfer status
