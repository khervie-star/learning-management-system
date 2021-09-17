from django.urls import path
from . import views, transfers

app_name = "wallet"

urlpatterns = [
    # payment endpoint

    # instantiate payment
    path('initiate/', views.initiate_payment),
    # verify payment
    path('verify/', views.verify_payment),

    # transfer endpoint

    # verify account details
    path('verify-account/', transfers.verify_account),

    # transfer webhook
    path('transfer/webhook/', transfers.transfer_status_webhook),
]
