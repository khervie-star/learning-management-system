from rest_framework import serializers

from review.models import Rating
from course.serializers import CourseSerializer


class RatingSerializer(serializers.ModelSerializer):
    course_slug = serializers.CharField(write_only=True)
    review = serializers.CharField(allow_null=True)

    class Meta:
        model = Rating
        exclude = ('course', )
        read_only_fields = (
            'rated_by', 'createed_at', 'updated_at'
        )
