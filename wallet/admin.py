from django.contrib import admin

from wallet.models import Wallet, Payment

admin.site.register((Wallet, Payment))
