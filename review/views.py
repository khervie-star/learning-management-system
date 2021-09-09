from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from review.serializers import RatingSerializer
from review.models import Rating

from instructor.models import Course
from student.models import Profile

# Just used to test the endpoint
User = get_user_model().objects.all()[0]


@api_view(['POST', 'GET', 'PATCH'])
def rate_course(request):
    # authenticated_user = User
    authenticated_user = request.user

    serializer = RatingSerializer
    # should send : 1. course_slug
    # :2. rating
    serialized_data = serializer(data=request.data)
    serialized_data.is_valid(raise_exception=True)

    if request.method == 'POST':
        slug = request.data["course_slug"]
        count = serialized_data.data["count"]

        try:
            course = Course.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return Response({"message": "The passed course_slug doesn't exist"}, status="404")
        else:
            is_enrolled = list(course.enrolled_students.values_list())
            for students in is_enrolled:
                if authenticated_user.name in students:
                    isRated = Rating.objects.filter(course=course, rated_by=authenticated_user)
                    if isRated.exists():
                        return Response({"message": "You have rated this course already. You probably should be calling the update endpoint or get"}, status="409")
                    else:
                        rating = Rating.objects.create(
                            course=course, rated_by=authenticated_user, count=count
                        )
                        serialized_response = serializer(rating).data
                        return Response({'message': "Rated", 'data': serialized_response})
                else:
                    return Response({"message": "Permission Denied. You are not enrolled in this course"})

    if request.method == 'GET':
        slug = request.data["course_slug"]
        try:
            course = Course.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return Response({"message": "The passed course_slug doesn't exist"}, status="404")
        else:
            rating = Rating.objects.filter(course=course, rated_by=authenticated_user)
            if not rating.exists():
                return Response({"message": "You have not rated this course"})
            else:
                serialized_data = serializer(rating.get()).data
                return Response({"data": serialized_data}, status="200")

    if request.method == 'PATCH':
        slug = request.data["course_slug"]
        count = request.data["count"]
        try:
            course = Course.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return Response({"message": "The passed course_slug doesn't exist"}, status="404")
        else:
            rating = Rating.objects.filter(course=course, rated_by=authenticated_user)
            if not rating.exists():
                return Response({"message": "You have not rated this course"})
            else:
                rating.update(count=count)
                data = Rating.objects.get(course=course, rated_by=authenticated_user)
                serialized_data = serializer(data).data
                return Response({"message": "Updated", "data": serialized_data}, status="200")
