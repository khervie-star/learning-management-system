from rest_framework import serializers
from instructor.models import Course, Lesson, Content


class CourseSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author_name')
    course_lessons = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all(), many=True)

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
            'created', 'updated', 'slug'
        )


class ContentSerializer(serializers.ModelSerializer):
    pass
