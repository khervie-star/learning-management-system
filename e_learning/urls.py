from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # user auth app
    path('user/', include("userauth.urls", )),
    # instructor app
    path('', include('instructor.urls')),
    #  catalog app
    path('catalog/', include('catalog.urls')),
]
