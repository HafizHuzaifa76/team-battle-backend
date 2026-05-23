from django.shortcuts import render
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView
from core.permissions import IsAdminRole
from core.utils.responses import success_response

from drf_spectacular.utils import extend_schema

from teams.models import Team
from teams.serializers import TeamSerializer
from teams.services import create_team, get_all_teams

# Create your views here.
class TeamListView(APIView):

    permission_classes = [IsAdminRole]

    def get(self, request):
        teams = get_all_teams()

        serializer = TeamSerializer(teams, many=True)

        return success_response(
            message='Teams Fetched Successfully',
            data=serializer.data,
            status_code=HTTP_200_OK
        )

    def post(self, request):

        serializer = TeamSerializer(request.data)
        serializer.is_valid(raise_exception=True)

        team = create_team(serializer.validated_data)

        response_seriaizer = TeamSerializer(team)

        return success_response(
            message='Team Created Successfully',
            data=response_seriaizer.data,
            status_code=HTTP_201_CREATED
        )