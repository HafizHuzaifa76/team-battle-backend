from dataclasses import field
from django.forms import CharField
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


from django.db import models

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model: User
        
        fields = [
            'email',
            'password',
            'role',
            'name'
        ]

    def create(self, validated_data):
        return User.objects.create_user( **validated_data)

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only = True
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        
        user = authenticate(
            email=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid credentials"
            )
        
        refresh = RefreshToken.for_user(user)

        return {

            "user": {

                "id": user.id,
                "email": user.email,
                "role": user.role,
            },

            "tokens": {

                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }

    class Meta:
        model: User
        fields = [
            'email',
            'password'
        ]