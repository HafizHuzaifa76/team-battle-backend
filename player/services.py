

from player.models import Player


def get_all_players():
    return Player.objects.all()

def create_player(validated_data):
    player = Player.objects.create(
        **validated_data
    )
    return player