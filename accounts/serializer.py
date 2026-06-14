
from dataclasses import field
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from teams.basic_serializers import TeamBasicSerializer
from .models import  Role, User


from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User

        fields = [
            'name',
            'email',
            'password',
            'role',
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only = True
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        
        user = authenticate(
            username=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid credentials"
            )

        # player_data = user.player

        
        refresh = RefreshToken.for_user(user)

        return {

            "user": user.to_json(),
            # "user": {
            #     "id": user.id,
            #     "name": user.name,
            #     "email": user.email,
            #     "role": user.role,
            #     if(user.role = Role.ADMIN) "team": user.team,
            # },

            # 'player': player_data,

            "tokens": {

                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }

    class Meta:
        model = User
        fields = [
            'email',
            'password'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'role'            
        ]

class PlayerSerializer(serializers.ModelSerializer):
    team = TeamBasicSerializer(read_only = True)
    class Meta:
        model = User
        fields = ['id','name', 'email', 'role', 'team']