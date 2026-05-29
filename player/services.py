

from player.models import Player


def get_all_players():
    return Player.objects.all()

def create_player(validated_data):
    return Player.object.create(validated_data)