from rest_framework import serializers
from instructor.models import Course, Lesson, Content


class CourseSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author_name')

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = (
            'author', 'slug',
        )

    def get_author_name(self, obj):
        return obj.author.name


class LessonSerializer(serializers.ModelSerializer):
    pass


class ContentSerializer(serializers.ModelSerializer):
    pass
