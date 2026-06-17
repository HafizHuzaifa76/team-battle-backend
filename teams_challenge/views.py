from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from core.utils.responses import success_response
from teams_challenge.serializers import ChallengeSerializer
from teams_challenge.services import create_challenge, get_challenge_by_id, get_challenges

# Create your views here.
class ChallengeListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChallengeSerializer

    def get(self, request):
        
        challenge = get_challenges()
        seializer = ChallengeSerializer(challenge, many=True)

        return success_response(
            message='Challenges fetched successfully',
            data=seializer.data,
        )

    def post(self, request):
        data = request.data
        
        seriaizer = ChallengeSerializer(data=request.data)
        seriaizer.is_valid(raise_exception=True)

        challenge = create_challenge(seriaizer.validated_data)
        response_seializer = ChallengeSerializer(challenge)

        return success_response(
            message='Challenge created successfully',
            data=response_seializer.data,
            status_code=HTTP_201_CREATED
        )

class ChallengeDetaiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChallengeSerializer

    def get(self, request, challenge_id):
        challenge = get_challenge_by_id(challenge_id)
        serializer = ChallengeSerializer(challenge)

        return success_response(
            message='Challenge fetch successfully',
            data=serializer.data
        )
