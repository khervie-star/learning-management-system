from django.urls import path
from . import views

app_name = "wallet"

urlpatterns = [
    # instantiate payment
    path('initiate/', views.initiate_payment),
    # verify payment
    path('verify/', views.verify_payment),
]
