from rest_framework import serializers
from course.models import Course, Lesson, CourseContent, TextContent


class CourseSerializer(serializers.ModelSerializer):
    # ratings = serializers.IntegerField()
    author = serializers.SerializerMethodField('get_author_name')
    course_lessons = serializers.SlugRelatedField(slug_field="slug", many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = (
            'author', 'slug', 'created', 'updated'
        )

    def get_author_name(self, obj):
        return obj.author.name


class LessonSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = (
            'created', 'updated', 'slug',
        )

#  not yet implemented


class VideoContentSerializer(serializers.ModelSerializer):
    pass


class TextSerializer(serializers.Serializer):
    related_lesson_slug = serializers.CharField()
    content = serializers.CharField()


class TextEditSerializer(serializers.Serializer):
    content = serializers.CharField()
