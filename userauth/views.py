from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate, logout, login
from django.core.exceptions import ObjectDoesNotExist
from userauth.serializers import RegisterSerializer , ChangePasswordSerializer, LoginSerializer
from userauth.models import CustomUser


class LoginView(APIView):
    serializer_class = LoginSerializer
    def post(self, request):
        data = request.data
        serialized_data = self.serializer_class(data=data)
        serialized_data.is_valid(raise_exception=True)
        try:
            user = authenticate(request, username=serialized_data.validated_data["email"], password=serialized_data.validated_data["password"])
        except ValueError:
            return Response({"message": "Invalid Login credentials"}, status="401")
            
        else:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            return Response({"message": "Login successful", "data":{
                'name': user.name,
                'email': user.email,
                'token': token.key
            }}, status="200")
            
class LogoutView(APIView):
    permission_class = [IsAuthenticated]
    authentication_class = [TokenAuthentication]
    def get(self, request):
        user = request.user
        Token.objects.get(user__id=user.id).delete()
        logout(request)
        return Response({"message": "Logged out successfully"}, status="200")

class ChangePasswordView(APIView):
    permission_class = [IsAuthenticated,]
    authentication_class = [TokenAuthentication,]
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        data = request.data
        user = request.user
        serialized_data = self.serializer_class(data=data)
        serialized_data.is_valid(raise_exception=True)
        password = serialized_data.validated_data["password"]
        user = CustomUser.objects.get(id=user.id)
        user.set_password(password)
        user.save()
        return Response({"message": "Password Updated"}, status="204")


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        data = request.data
        serialized_data = self.serializer_class(data=data)
        serialized_data.is_valid(raise_exception=True)
        
        user = CustomUser.objects.create_user(email=serialized_data.validated_data["email"],
            name=serialized_data.validated_data["name"], password=serialized_data.validated_data["password"]
        )
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"message": "Account Created Successfully", "data":{
                'name': user.name,
                'email': user.email,
                'token': token.key
           }}, status="200")
