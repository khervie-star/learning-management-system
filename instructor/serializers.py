from rest_framework import serializers
from instructor.models import Course, Lesson, Content

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        extra_fields = {
            'author': read_only,
            'slug': read_only,
        }

class LessonSerializer(serializers.ModelSerializer):
    pass

class ContentSerializer(serializers.ModelSerializer):
    pass
