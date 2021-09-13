from django.contrib import admin

from instructor.models import Instructor

admin.site.register((Instructor, ))
