from django.urls import path

from student import views

app_name = "student"

urlpatterns = [
    #  profile ['GET']
    path('profile', views.profile,),
    # profile ['PATCH', 'POST']
    path('create-update/', views.create_update_profile,),
]
