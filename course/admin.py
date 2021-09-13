from django.contrib import admin
from course.models import Category, Course, Lesson, CourseContent, VideoContent, TextContent

admin.site.register((Category, Course, Lesson, CourseContent, TextContent, VideoContent))
