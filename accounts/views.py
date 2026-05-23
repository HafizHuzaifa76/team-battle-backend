from django.shortcuts import render
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView

from .models import User

from .permissions import IsAdminRole
from .serializer import LoginSerializer, RegisterSerializer, UserSerializer
from core.utils.responses import success_response

from drf_spectacular.utils import extend_schema

# Create your views here.


class UsersView(APIView):

    permission_classes = [IsAdminRole]
    
    def get(self, request):

        users = User.objects.all()

        serializer = UserSerializer(users, many=True)

        return success_response(
            message="Login successfully",
            data=serializer.data,
            status_code=HTTP_200_OK
        )

@extend_schema(
    request=RegisterSerializer
)
class RegisterUserView(APIView):

    permission_classes = [IsAdminRole]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return success_response(
            message="User created successfully",
            data={

                "user": {

                    "id": user.id,
                    "email": user.email,
                    "role": user.role
                }
            },
            status_code=HTTP_201_CREATED
        )

@extend_schema(
    request=LoginSerializer
)
class LoginUserView(APIView):
    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        return success_response(
            message="Login successfully",
            data=serializer.validated_data,
            status_code=HTTP_200_OK
        )

