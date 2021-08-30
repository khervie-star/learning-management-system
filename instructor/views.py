from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from instructor.serializers import CourseSerializer, LessonSerializer
from instructor.models import Course

USER = get_user_model()


class CourseView(APIView):
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs):
        _slug = kwargs.get("slug", None)
        if not _slug:
            # get all courses
            courses = Course.objects.all()
            serialized_object = self.serializer_class(courses, many=True)
            return Response({"data": serialized_object.data}, status="200")
        else:
            # get a  single course instance
            try:
                course = Course.objects.get(slug=_slug)
            except ObjectDoesNotExist:
                return Response({"status": "Failed", "message": " The object accessed does not exist"}, status="404")
            else:
                serialized_object = self.serializer_class(course)
                return Response({"data": serialized_object.data}, status="200")

    def post(self, request):
        received_course_data = request.data
        serialized_data = self.serializer_class(data=received_course_data)
        serialized_data.is_valid(raise_exception=True)
        if serialized_data.errors:
            return Response({"error": serialized_data.errors})
        else:
            # testing
            # serialized_data.save(author=USER.objects.get(name="Dev Admin"))
            serialized_data.save(author=request.user)
            return Response({"status": "Success", "Message": "Course created successfully", "data": serialized_data.data}, status="201")

    def patch(self, request, *args, **kwargs):
        _slug = kwargs.get("slug", None)
        if not _slug:
            return Response({"error": "method /PATCH/ not allowed"}, status="405")
        try:
            course_object = Course.objects.get(slug=_slug)
        except ObjectDoesNotExist:
            return Response({"error": "method /PATCH/ not allowed"}, status="405")
        else:
            serialized_data = self.serializer_class(
                instance=course_object, data=request.data, partial=True)
            serialized_data.is_valid(raise_exception=True)
            serialized_data.save()
            return Response({'message': 'Update successful', "data": serialized_data.data}, status="200")

    def delete(self, request, *args, **kwargs):
        slug_ = kwargs.get("id", None)
        if not slug_:
            return Response({"error": "method /DELETE/ not allowed"}, status="405")
        try:
            course_object = Course.objects.get(slug=slug_)
        except ObjectDoesNotExist:
            return Response({"error": "method /DELETE/ not allowed"}, status="405")
        else:
            course_object.delete()
            return Response({"message": "Course deleted"}, status="200")


class LessonView(APIView):
    pass


class ContentView(APIView):
    pass


@api_view([])
def add_student_to_course(request):
    pass
