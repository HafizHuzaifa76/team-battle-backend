from django.forms import ValidationError
from rest_framework import serializers
from accounts.basic_serializers import PlayerBasicSerializer
from accounts.models import Role, User
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
        print('team')
        print(team)

        qs = User.objects.filter(id__in = value, role = Role.PLAYER, team__isnull = False)
        print('qs')
        print(qs)

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

        read_only_fields = ['rank', 'category', 'identifier', 'players']
