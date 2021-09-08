from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from instructor.models import Course
from instructor.serializers import CourseSerializer


@api_view([])
def filter_course(request, *args, **kwargs):
    """
        create a way to categorize courses
    """

    filter_fields = ('category', 'level', 'price', )
    print(kwargs["filter"])
    return Response({})


@api_view(["GET"])
def search_course(request, *args, **kwargs):
    serializer = CourseSerializer
    search_keyword = request.GET.get("q")
    retrieved_data = Course.objects.filter(
        Q(name__icontains=search_keyword) |
        Q(name__iexact=search_keyword) |
        Q(name__istartswith=search_keyword) |
        Q(name__iendswith=search_keyword)
    )
    if not retrieved_data:
        return Response({"data": []}, status="200")
    serialized_data = serializer(retrieved_data, many=True)
    return Response({"data": serialized_data.data}, status="200")
