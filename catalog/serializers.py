from rest_framework import serializers


class FilterSerializer(serializers.Serializer):
    level = serializers.CharField(required=False)
    # by programs and free courses <- to be added later
    # by price
    categories = serializers.CharField(required=False)
