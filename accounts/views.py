from django.shortcuts import render
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView

from .permissions import IsAdminRole
from .serializer import LoginSerializer, RegisterSerializer
from core.utils.responses import success_response

# Create your views here.
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