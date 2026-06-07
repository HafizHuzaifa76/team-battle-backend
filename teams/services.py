

from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework.generics import _get_object_or_404
from accounts.models import User
from player.models import Player
from teams.models import Team


def create_team(validated_data):
    last_team = Team.objects.order_by('-rank').first()

    next_rank = 1
    if last_team:
        next_rank = last_team.rank + 1
    
    name = validated_data.get('name')
    player_ids = validated_data.get('player_ids')
    identifier = '_'.join(str(name).strip().lower().split())

    team = Team.objects.create(
        name=name,
        identifier=identifier,
        rank=next_rank
    )

    Player.objects.filter(id__in = player_ids, team__isnull=True).update(team=team)

    # User.objects.create_user(
    #     email = identifier,
    #     password = 'player123'
    # )

    

    return team

def edit_team(team_id, validated_data):
    team = get_object_or_404(Team, id=team_id)
    
    new_player_ids = validated_data.get('player_ids')

    for key, value in validated_data.items():
        setattr(team, key, value)
    
    team.save()

    Player.objects.filter(team=team).exclude(
        id__in=new_player_ids
    ).update(team=None)

    Player.objects.filter(
        id__in=new_player_ids,
        team__isnull=True
    ).update(team=team)

    return team

def delete_team(team_id):
    team = get_object_or_404(Team, id=team_id)
    team.delete()

def get_all_teams():
    teams = Team.objects.all()

    return teams

def get_team_by_id(team_id):
    try:
        return Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        raise NotFound("Team Not Found")