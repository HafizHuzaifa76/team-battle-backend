from rest_framework import serializers
from teams.models import Team

class TeamBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            'id',
            'name',
            'identifier',
            'category',
            'rank'
        ]