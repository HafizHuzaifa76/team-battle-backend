from rest_framework import serializers

from teams.models import Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            'id',
            'name',
            'rank'
        ]
        read_only_fields = ['rank']