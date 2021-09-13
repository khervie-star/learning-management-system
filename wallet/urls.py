from django.urls import path
from . import views

app_name = "wallet"

urlpatterns = [
    path('initiate/', views.initiate_payment),
]
