

from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from accounts.models import Role, User


def get_all_players():
    return User.objects.filter(role = Role.PLAYER)
    
def get_player_by_id(player_id):
    try:
        return User.objects.get(id = player_id, role = Role.PLAYER)
    except User.DoesNotExist:
        raise NotFound('Player Not Found')

def create_player(validated_data):
    email = validated_data.get("email")
    name = validated_data.get("name")
    
    if User.objects.filter(email = email).exists():
        raise Exception('User with this email already exist')

    user = User.objects.create_user(
        name = name,
        email = email,
        role = Role.PLAYER,
        password = 'player123'
    )

    return user

def edit_player(player_id, validated_data):
    player = get_object_or_404(User, id = player_id, role = Role.PLAYER)

    for key, value in validated_data.items():
        setattr(player, key, value)

    player.save()

    return player

def delete_player(player_id):
    player = get_object_or_404(User, id = player_id, role = Role.PLAYER)

    player.delete()
    