from django.urls import path
from . import views

app_name = "userauth"

urlpatterns = [
    # register endpoint - handles post request
    path('register/', views.RegisterView.as_view()),
    # login endpoint - handles post request
    path('login/', views.LoginView.as_view()),
    # logout endpoint - handles get request
    path('logout/', views.LogoutView.as_view()),
    # change password endpoint - handles put request
    path('chnage-password/', views.ChangePasswordView.as_view()),
]