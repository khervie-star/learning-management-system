import copy
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404

from course.models import Course, Category
from course.serializers import CourseSerializer
from catalog.serializers import FilterSerializer


@api_view(['GET'])
def filter_course(request, *args, **kwargs):
    serializer = FilterSerializer

    received_filters = request.data
    serialized_data = serializer(data=received_filters)
    serialized_data.is_valid(raise_exception=True)

    if len(serialized_data.data) == 0:
        return Response({"data": []}, status="200")

    if serialized_data.data["categories"]:
        category = serialized_data.data["categories"]
        category = get_object_or_404(Category, name__iexact=category)
        filter = copy.deepcopy(serialized_data.data)
        del filter["categories"]
        filtered_courses = Course.objects.filter(
            categories=category, **filter)

        if filtered_courses.exists():
            serialized_data = CourseSerializer(filtered_courses, many=True)
            return Response({"data": serialized_data.data}, status="200")
        else:
            return Response({"data": []}, status="200")

    else:
        filtered_courses = Course.objects.filter(**serialized_data.data)
        if filtered_courses.exists():
            serialized_data = CourseSerializer(
                data=filtered_courses, many=True).is_valid(raise_exception=True)
            return Response({"data": serialized_data.data}, status="200")
        else:
            return Response({"data": []}, status="200")


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
