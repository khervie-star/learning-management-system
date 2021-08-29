from django.contrib import admin
from instructor.models import DummyModel, Course, Lesson, Content, VideoContent, TextContent

admin.site.register((DummyModel, Course, Lesson, Content, TextContent, VideoContent))