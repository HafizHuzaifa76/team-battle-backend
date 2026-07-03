from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView

from accounts import serializer
from accounts.serializer import PlayerSerializer
from core.permissions import IsAdminRole
from accounts.player_service import create_player, delete_player, edit_player, get_all_players, get_player_by_id  
from core.utils.responses import error_response, success_response

from drf_spectacular.utils import extend_schema

# Create your views here.
class PlayersListView(APIView):

    serializer_class = PlayerSerializer
    
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminRole()]
        return [IsAuthenticated()]

    def get(self, request):
        players = get_all_players()
        serializer = PlayerSerializer(players, many=True)

        return success_response(
            message = 'Players Fetched Successfully',
            data = serializer.data,
            status_code=HTTP_200_OK
        )
    
    def post(self, request):
        try:
            serializer = PlayerSerializer(data=request.data)
            serializer.is_valid(raise_exception = True)

            player = create_player(validated_data = serializer.validated_data)
            response_serializer = PlayerSerializer(player)

            return success_response(
                message = 'Player Created Successfully', 
                data = response_serializer.data,
                status_code = HTTP_201_CREATED
            )
        except Exception as e:
            return error_response(
                message = str(e)
            )

class PlayerrDetailView(APIView):

    serializer_class = PlayerSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]

    def get(self, request, id):
        player = get_player_by_id(id)
        serializer = PlayerSerializer(player)

        return success_response(
            message = 'Player Fetched Successfully',
            data = serializer.data
        )

    def patch(self, request, id):
        player = get_player_by_id(id)
        serializer = PlayerSerializer(player, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        player = edit_player(player_id=id, validated_data=serializer.validated_data)
        response_serializer = PlayerSerializer(player)

        return success_response(
            message = 'Player Updated Successfully',
            data = response_serializer.data
        )
    
    def delete(self, request, id):
        delete_player(player_id = id)
        return success_response(
            message = 'Player Deleted Successfully'
        )
