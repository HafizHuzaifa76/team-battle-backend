

from django.shortcuts import get_object_or_404
from accounts.models import User
from player.models import Player


def get_all_players():
    return Player.objects.all()

def create_player(validated_data):
    email = validated_data.get("email")
    
    if Player.objects.filter(email = email).exists():
        raise Exception('Player with this email already exist')

    # user = User.objects.create_user(
    #     email = email,
    #     password = 'player123'
    # )

    player = Player.objects.create(
        **validated_data
    )

    return player

def edit_player(player_id, validated_data):
    player = get_object_or_404(Player, id = player_id)
    
    for key, value in validated_data.items():
        setattr(player, key, value)
    
    player.save()
    return player

def delete_player(player_id):
    player = get_object_or_404(Player, id = player_id)

    player.delete()
    