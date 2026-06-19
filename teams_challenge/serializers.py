from teams_challenge.basic_serializers import ChallengeBaseSerializer


class ChallengeCreateSerializer(ChallengeBaseSerializer):
    class Meta(ChallengeBaseSerializer.Meta):
        read_only_fields = ChallengeBaseSerializer.Meta.read_only_fields + [
            "winner",
            "status",
            "challenger_points",
            "challenged_points",
        ]