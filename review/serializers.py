from rest_framework import serializers

from review.models import Rating
from instructor.serializers import CourseSerializer


class RatingSerializer(serializers.ModelSerializer):
    course_slug = serializers.CharField(write_only=True)

    class Meta:
        model = Rating
        exclude = ('course', )
        read_only_fields = (
            'rated_by',
        )
