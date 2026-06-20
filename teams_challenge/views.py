
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView

from core.permissions import IsAdminRole
from core.utils.responses import success_response
from teams_challenge.basic_serializers import ChallengeBaseSerializer
from teams_challenge.serializers import ChallengeCreateSerializer, ChallengeResultSerializer
from teams_challenge.services import create_challenge, get_challenge_by_id, get_challenges, update_challenge_result

# Create your views here.
class ChallengeListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChallengeCreateSerializer

    def get(self, request):
        
        challenge = get_challenges()
        seializer = ChallengeBaseSerializer(challenge, many=True)

        return success_response(
            message='Challenges fetched successfully',
            data=seializer.data,
        )

    def post(self, request):
        data = request.data
        
        seriaizer = ChallengeCreateSerializer(data=request.data)
        seriaizer.is_valid(raise_exception=True)

        challenge = create_challenge(seriaizer.validated_data)
        response_seializer = ChallengeCreateSerializer(challenge)

        return success_response(
            message='Challenge created successfully',

            data=response_seializer.data,
            status_code=HTTP_201_CREATED
        )

class ChallengeDetaiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChallengeBaseSerializer

    def get(self, request, challenge_id):
        challenge = get_challenge_by_id(challenge_id)
        serializer = ChallengeBaseSerializer(challenge)

        return success_response(
            message='Challenge fetch successfully',
            data=serializer.data
        )


    def patch(self, request, challenge_id):
        seriaizer = ChallengeCreateSerializer(data=request.data, partial=True)
        seriaizer.is_valid(raise_exception=True)

        challenge = create_challenge(seriaizer.validated_data)
        response_seializer = ChallengeCreateSerializer(challenge)

        return success_response(
            message='Challenge created successfully',

            data=response_seializer.data,
            status_code=HTTP_201_CREATED
        )
        

class ChallengeResultView(APIView):
    permission_classes = [IsAdminRole]
    serializer_class = ChallengeResultSerializer

    def patch(self, request, challenge_id):
        seriaizer = ChallengeResultSerializer(data=request.data)
        seriaizer.is_valid(raise_exception=True)

        challenge = update_challenge_result(seriaizer.validated_data, challenge_id)
        response_seializer = ChallengeResultSerializer(challenge)

        return success_response(
            message='Challenge commpleted successfully',
            data=response_seializer.data,
            status_code=HTTP_200_OK
        )
        