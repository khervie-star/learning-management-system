from django.urls import path

from review import views

app_name = "review"

urlpatterns = [
    # rate endpoints = ['POST', 'GET', 'PATCH']
    path('', views.rate_course),
    # rating average ['GET']
    path('average/', views.course_average_rating),

]
