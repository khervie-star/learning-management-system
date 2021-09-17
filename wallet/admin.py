from django.contrib import admin

from wallet.models import Wallet, Payment, Transfers, TransactionLog

admin.site.register((Wallet, Payment, Transfers, TransactionLog))
