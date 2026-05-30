

from django.shortcuts import get_object_or_404
from rest_framework.generics import _get_object_or_404
from teams.models import Team


def create_team(validated_data):
    last_team = Team.objects.order_by('-rank').first()

    next_rank = 1
    if last_team:
        next_rank = last_team.rank + 1

    team = Team.objects.create(
        name=validated_data['name'],
        rank=next_rank
    )

    return team

def edit_team(team_id, validated_data):
    team = get_object_or_404(Team, id=team_id)
    
    for key, value in validated_data.items():
        setattr(team, key, value)
    
    team.save()
    return team

def delete_team(team_id):
    team = get_object_or_404(Team, id=team_id)
    team.delete()

def get_all_teams():
    teams = Team.objects.all()

    return teams