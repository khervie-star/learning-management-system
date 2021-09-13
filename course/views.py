from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from course.serializers import CourseSerializer, LessonSerializer, TextSerializer, TextEditSerializer
from course.models import Course, Lesson, CourseContent, TextContent, VideoContent
from student.models import Profile

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
        slug_ = kwargs.get("slug", None)
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
    # add permissions and authorization
    # slug: -> course slug
    serializer_class = LessonSerializer

    def get(self, request, *args, **kwargs):
        related_course_slug = kwargs.get("related_course_slug", None)
        lesson_slug = kwargs.get("lesson_slug", None)
        if lesson_slug:
            # get a  single lesson instance
            try:
                lesson = Lesson.objects.get(slug=lesson_slug)
            except ObjectDoesNotExist:
                return Response({"message": "The object reference/ slug passed does not exists"}, status="405")
            else:
                serialized_object = self.serializer_class(lesson)
                return Response({"data": serialized_object.data}, status="200")

        if related_course_slug:
            # get all lessons associated to a course
            lessons = Lesson.objects.filter(course__slug=related_course_slug)
            if not lessons.exists():
                return Response({"status": "Failed", "message": "The object accessed does not exist"}, status="404")
            else:
                serialized_object = self.serializer_class(lessons, many=True)
                return Response({"data": serialized_object.data}, status="200")

    def post(self, request):
        received_lesson_data = request.data
        serialized_data = self.serializer_class(data=received_lesson_data)
        serialized_data.is_valid(raise_exception=True)
        if serialized_data.errors:
            return Response({"error": serialized_data.errors})
        else:
            # testing
            # serialized_data.save(author=USER.objects.get(name="Dev Admin"))
            serialized_data.save(author=request.user)
            return Response({"status": "Success", "Message": "Course created successfully", "data": serialized_data.data}, status="201")

    def patch(self, request, *args, **kwargs):
        related_course_slug = kwargs.get("related_course_slug", None)
        if not _slug:
            return Response({"error": "method /PATCH/ not allowed"}, status="405")
        try:
            lesson_object = Lesson.objects.get(course__slug=related_course_slug)
        except ObjectDoesNotExist:
            return Response({"error": "method /PATCH/ not allowed"}, status="405")
        else:
            serialized_data = self.serializer_class(
                instance=lesson_object, data=request.data, partial=True)
            serialized_data.is_valid(raise_exception=True)
            serialized_data.save()
            return Response({'message': 'Update successful', "data": serialized_data.data}, status="200")

    def delete(self, request, *args, **kwargs):
        slug_ = kwargs.get("related_course_slug", None)
        if not slug_:
            return Response({"error": "method /DELETE/ not allowed"}, status="405")
        try:
            lesson_object = Lesson.objects.get(course__slug=slug_)
        except ObjectDoesNotExist:
            return Response({"error": "method /DELETE/ not allowed"}, status="405")
        else:
            lesson_object.delete()
            return Response({"message": "Course deleted"}, status="200")


@api_view(['POST'])
def course_enrollment(request, *args, **kwargs):
    model = Course
    authenticated_user = request.user

    # adding the student to to course set
    course_slug = request.data["course_slug"]
    course_instance = get_object_or_404(model, slug=course_slug)
    course_instance.enrolled_students.add(authenticated_user)

    # adding the course to the student profile course set
    user = get_object_or_404(Profile, user=authenticated_user)
    user.courses.add(course_instance)

    return Response({"message": "Enrolled successfully"}, status="200")


@api_view(["POST"])
def create_text_content(request):
    serializer = TextSerializer
    serialized_data = serializer(data=request.data)
    serialized_data.is_valid(raise_exception=True)
    related_lesson = serialized_data["related_lesson_slug"].value
    try:
        lesson = Lesson.objects.get(slug=related_lesson)
    except ObjectDoesNotExist:
        return Response({"status": "Failed", "message": "The object received related_lesson_slug does not exist"}, status="404")
    else:
        text_instance = TextContent.objects.create(content=serialized_data["content"].value)
        content_instance = Content(target=text_instance, lesson=lesson)
        content_instance = content_instance.save()
    return Response({"message": "Text Content Created", "data": serialized_data.data, "content_type": content_instance.content_object}, status="200")


@api_view(['PATCH', 'GET', 'DELETE'])
def get_edit_delete_text_content(request, id, *args, **kwargs):

    serializer = TextEditSerializer

    try:
        text_instance = TextContent.objects.get(id=id)
    except ObjectDoesNotExist:
        return Response({"message": "The id passed is not valid"}, status="404")
    else:

        if request.method == 'GET':
            serialized_data = serializer(text_instance)
            return Response({"data": serialized_data.data}, status="200")

        elif request.method == 'DELETE':
            text_instance.delete()
            return Response({"message": "Content Deleted"}, status="200")

        elif request.method == 'PATCH':
            received_data = request.data
            serialized_data = serializer(data=received_data)
            serialized_data.is_valid(raise_exception=True)
            TextContent.objects.filter(id=text_instance.id).update(**serialized_data.data)
            return Response({"message": "Updated Content"}, status="200")
        else:
            pass


@api_view(["GET"])
def available_categories(request):
    pass
