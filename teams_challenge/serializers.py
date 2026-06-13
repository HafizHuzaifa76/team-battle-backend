
from rest_framework import serializers

from teams.basic_serializers import TeamBasicSerializer
from teams_challenge.models import Challenge

class ChallengeSerializer(serializers.ModelSerializer):
    challenger = TeamBasicSerializer()
    challenged = TeamBasicSerializer()

    class Meta:
        model = Challenge
        fields = "__all__"

        read_only_fields = [
            'winner',
            'challenger_points',
            'challenged_points',
            'updated_at',
            'created_at',
        ]