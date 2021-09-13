from django.contrib import admin
# from course.models import Category, Course, Lesson, Content, VideoContent, TextContent
#
# admin.site.register((Category, Course, Lesson, Content, TextContent, VideoContent))

from course.models import Course

admin.site.register(Course)
