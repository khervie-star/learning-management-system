from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # user auth app
    path('user/', include("userauth.urls", )),
    # instructor app
   path('instructor/', include('instructor.urls')),
]
