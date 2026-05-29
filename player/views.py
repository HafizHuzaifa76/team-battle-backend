from django.shortcuts import render
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView

from core.permissions import IsAdminRole
from player.serializers import PlayerSerializer
from player.services import create_player, get_all_players
from core.utils.responses import success_response

from drf_spectacular.utils import extend_schema

# Create your views here.
@extend_schema(
    request=PlayerSerializer
)
class PlayersListView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        players = get_all_players()
        serializer = PlayerSerializer(players, many=True)

        return success_response(
            message = 'Players Fetched Successfully',
            data = serializer.data,
            status_code=HTTP_200_OK
        )
    
    def post(self, request):
        serializer = PlayerSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)

        player = create_player(validated_data = serializer.validated_data)
        response_serializer = PlayerSerializer(player)

        return success_response(
            message = 'Player Created Successfully', 
            data = response_serializer.data,
            status_code = HTTP_201_CREATED
        )