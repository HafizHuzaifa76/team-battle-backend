from django.shortcuts import render
from django.views.generic import edit
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView
from core.permissions import IsAdminRole
from core.utils.responses import error_response, success_response

from drf_spectacular.utils import extend_schema

from teams.models import Team
from teams.serializers import TeamSerializer
from teams.services import create_team, delete_team, edit_team, get_all_teams, get_team_by_id

# Create your views here.
@extend_schema(
    request=TeamSerializer
)
class TeamListView(APIView):

    permission_classes = [IsAdminRole]
    serializer_class = TeamSerializer

    def get(self, request):
        teams = get_all_teams()

        serializer = TeamSerializer(teams, many=True)

        return success_response(
            message='Teams Fetched Successfully',
            data=serializer.data
        )

    def post(self, request):

        serializer = TeamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        team = create_team(validated_data=serializer.validated_data)

        response_seriaizer = TeamSerializer(team)

        return success_response(
            message='Team Created Successfully',
            data=response_seriaizer.data,
            status_code=HTTP_201_CREATED
        )


class TeamDetailView(APIView):

    serializer_class = TeamSerializer
    permission_classes = [IsAdminRole]

    def get(self, request, id):
        team = get_team_by_id(team_id=id,)

        response_serializer = TeamSerializer(team)

        return success_response(
            message = 'Team Fetch Successfully',
            data = response_serializer.data
        )
            
    def patch(self, request, id):
        
        serializer = TeamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        team = edit_team(team_id=id, validated_data=serializer.validated_data)

        response_serializer = TeamSerializer(team)

        return success_response(
            message = 'Team Edit Successfully',
            data = response_serializer.data
        )
    
    def delete(self, request, id):
        delete_team(team_id = id)

        return success_response(
            message = 'Team Deleted Successfully' 
        )
