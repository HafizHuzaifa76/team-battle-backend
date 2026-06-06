from rest_framework import serializers

from player.models import Player
from teams.basic_serializers import TeamBasicSerializer

class PlayerSerializer(serializers.ModelSerializer):
    team = TeamBasicSerializer(read_only = True)
    class Meta:
        model = Player
        fields = ['id','name', 'age', 'email', 'team']