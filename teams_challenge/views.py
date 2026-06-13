from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from core.utils.responses import success_response
from teams_challenge.serializers import ChallengeSerializer
from teams_challenge.services import create_challenge, get_challenges

# Create your views here.
class ChallengeListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChallengeSerializer

    def get(self, request):
        
        challenge = get_challenges()
        seializer = ChallengeSerializer(challenge)

        return success_response(
            message='Challenges get successfully',
            data=seializer.data,
        )

    def post(self, request):
        data = request.data
        
        seriaizer = ChallengeSerializer(data=request.data)
        seriaizer.is_valid(raise_exception=True)
        challenge = create_challenge(seriaizer.validated_data)
        response_seializer = ChallengeSerializer(challenge)
        return success_response(
            message='Challenges get successfully',
            data=response_seializer.data,
            status_code=HTTP_201_CREATED
        )