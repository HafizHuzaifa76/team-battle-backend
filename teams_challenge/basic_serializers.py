from rest_framework import serializers
from teams.basic_serializers import TeamBasicSerializer
from teams.models import Team
from teams_challenge.models import Challenge

class ChallengeBaseSerializer(serializers.ModelSerializer):
    challenger_id = serializers.IntegerField(write_only=True)
    challenged_id = serializers.IntegerField(write_only=True)
    challenger = TeamBasicSerializer(read_only=True)
    challenged = TeamBasicSerializer(read_only=True)

    class Meta:
        model = Challenge
        fields = "__all__"
        read_only_fields = [
            "challenger",
            "challenged",
            "updated_at",
            "created_at",
        ]