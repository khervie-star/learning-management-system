from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view


class CourseView(APIView):
    pass

class LessonView(APIView):
    pass

class ContentView(APIView):
    pass

@api_view([])
def add_student_to_course(request):
    pass
