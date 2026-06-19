
from rest_framework import serializers
from teams_challenge.basic_serializers import ChallengeBaseSerializer


class ChallengeCreateSerializer(ChallengeBaseSerializer):
    challenger_id = serializers.IntegerField(write_only=True)
    challenged_id = serializers.IntegerField(write_only=True)
    
    class Meta(ChallengeBaseSerializer.Meta):
        read_only_fields = ChallengeBaseSerializer.Meta.read_only_fields + [
            "winner",
            "status",
            "challenger_points",
            "challenged_points",
        ]

class ChallengeResultSerializer(ChallengeBaseSerializer):
    class Meta(ChallengeBaseSerializer.Meta):
        read_only_fields = ChallengeBaseSerializer.Meta.read_only_fields + [
            "winner",
            "status",
            "challenge_date",
        ]