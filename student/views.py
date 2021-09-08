from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from student.serializers import ProfileSerializer
from student.models import Profile

User = get_user_model()


@api_view(['GET'])
def profile(request):
    authenticated_user = request.user
    serializer = ProfileSerializer

    _profile = get_object_or_404(Profile, user=authenticated_user)
    serialized_data = serializer(_profile)
    return Response({"data": serialized_data.data}, status="200")


@api_view(['PATCH', 'POST'])
def create_update_profile(request):
    authenticated_user = request.user
    received_data = request.data
    serializer = ProfileSerializer

    if request.method == 'POST':
        serialized_data = serializer(received_data)
        serialized_data.is_valid(raise_exception=True)

        serialized_data = serialized_data.data
        profile = Profile.objects.create(user=authenticated_user, **serialized_data)

        serialized_profile = serializer(profile)

        return Response({"message": "Profile Created", "data": serialized_profile.data}, status="201")

    if request.method == 'PATCH':
        serialized_data = serializer(received_data)
        serialized_data.is_valid(raise_exception=True)

        profile_instance = get_object_or_404(Profile, user=authenticated_user)
        profile_instance.update(**received_data)
        return Response({"message": "Profile updated"}, status="200")
