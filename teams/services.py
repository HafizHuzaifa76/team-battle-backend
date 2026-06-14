

from typing import Any


from unicodedata import category
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import _get_object_or_404
from accounts.models import Role, User
from teams.models import Category, Team


def create_team(validated_data):
    last_team = Team.objects.order_by('-rank').first()

    next_rank = 1
    if last_team:
        next_rank = last_team.rank + 1

    match next_rank:
        case rank if rank < 5:
            category = Category.PLATINUM

        case rank if rank < 22:
            category = Category.GOLD

        case rank if rank < 33:
            category = Category.SILVER

        case _:
            category = Category.BRONZE


    
    name = validated_data.get('name')
    player_ids = validated_data.get('player_ids')
    identifier = '_'.join(str(name).strip().lower().split())


    players = User.objects.filter(id__in = player_ids, role = Role.PLAYER, team__isnull=True)

    found_ids = set(players.values_list('id', flat=True))
    missing_ids = set(player_ids) - found_ids

    if missing_ids:
        raise ValidationError(f"Invalid Players IDs: {missing_ids}")

    team = Team.objects.create(
        name=name,
        identifier=identifier,
        category=category,
        rank=next_rank
    )

    players.update(team=team)

    return team

def edit_team(team_id, validated_data):
    team = get_object_or_404(Team, id=team_id)
    
    new_player_ids = validated_data.get('player_ids')

    players = User.objects.filter(id__in = new_player_ids, role = Role.PLAYER, team__isnull=True)

    found_ids = set(players.values_list('id', flat=True))
    missing_ids = set(new_player_ids) - found_ids
    print("Invalid Players IDs: {missing_ids}")

    if missing_ids:
        raise ValidationError(f"Invalid Players IDs: {missing_ids}")

    for key, value in validated_data.items():
        setattr(team, key, value)
    
    team.save()

    User.objects.filter(team=team).exclude(
        id__in=new_player_ids,
        role = Role.PLAYER,
    ).update(team=None)

    players.update(team=team)

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