from rest_framework import serializers

from player.models import Player

class PlayerBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id','name', 'age', 'email']