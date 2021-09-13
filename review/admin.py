from django.contrib import admin

from review.models import Rating

admin.site.register((Rating,))
