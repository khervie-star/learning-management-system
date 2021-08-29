from rest_framework import serializers
from userauth.models import CustomUser

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    
    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({'password': 'password mismatch'})
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    # add check for old password
    # old_password = serializers.CharField()
    password = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({'password': 'password mismatch'})
        return data
