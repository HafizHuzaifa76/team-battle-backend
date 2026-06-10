from django.forms import ValidationError
from rest_framework import serializers
from player.basic_serializers import PlayerBasicSerializer
from player.models import Player
from teams.models import Team

class TeamSerializer(serializers.ModelSerializer):
    player_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )

    players = PlayerBasicSerializer(many=True, read_only=True)

    def validate_player_ids(self, value):
        print(f'validating player ids: {len(value)}')
        
        if len(value) == 0:
            raise serializers.ValidationError(
                "At least one player is required."
            )
        
        team = self.instance

        qs = Player.objects.filter(id__in = value, team__isnull = False)

        if team:
            qs = qs.exclude(team = team)
        
        if qs.exists():
            raise serializers.ValidationError(
                "Some players already belong to another team."
            )

        return value
        
    class Meta:
        model = Team

        fields = [
            'id',
            'name',
            'identifier',
            'rank',
            'category',
            'player_ids',
            'players',
        ]

        read_only_fields = ['rank', 'category', 'identifier']
