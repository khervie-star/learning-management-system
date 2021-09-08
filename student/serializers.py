from rest_framework.serializers import ModelSerializer

from student.models import Profile


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = (
            'courses', 'user'
        )
