from rest_framework.serializers import ModelSerializer

from student.models import Profile
from course.serializers import CourseSerializer


class ProfileSerializer(ModelSerializer):
    courses = CourseSerializer(many=True)

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = (
            'courses', 'user'
        )
