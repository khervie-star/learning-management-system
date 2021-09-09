from django.urls import path

from review import views

app_name = "review"

urlpatterns = [
    # rate endpoints = ['POST', 'GET']
    path('', views.rate_course),
]
