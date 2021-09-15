from django.contrib import admin

from wallet.models import Wallet, Payment, Transfers

admin.site.register((Wallet, Payment, Transfers))
