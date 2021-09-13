from django.urls import path
from catalog import views

app_name = "catalog"

urlpatterns = [
    # ['GET']
    path('search', views.search_course),
    # ['GET']
    path('filter', views.filter_course),
]
