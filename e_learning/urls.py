from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # user auth app
    path('user/', include("userauth.urls", )),
    # instructor app
    # path('', include('course.urls')),
    #  catalog app
    # path('catalog/', include('catalog.urls')),
    # # student app
    # path('me/', include('student.urls')),
    # # Review / Rating app
    # path('ratings/', include('review.urls')),
    # # Wallet app
    # path('payment/', include('wallet.urls')),
]
