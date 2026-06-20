

from datetime import date
from django.shortcuts import get_object_or_404
from teams.models import Team
from django.db import transaction
from django.db.models import F
from teams_challenge.models import Challenge, ChallengeStatus, Winner
from rest_framework.exceptions import NotFound, ValidationError

def create_challenge(validated_data):
    challenger_team = validated_data.get('challenger_id')
    challenged_team = validated_data.get('challenged_id')
    challenge_date = validated_data.get('challenge_date')

    try:
        challenger = Team.objects.get(id=challenger_team)
    except Team.DoesNotExist:
        raise NotFound("Challenger Team Not Found")

    try:
        challenged = Team.objects.get(id=challenged_team)
    except Team.DoesNotExist:
        raise NotFound("Challenged Team Not Found")

    if challenger_team == challenged_team:
        raise ValidationError(
            'Team cannot challenge itself'
        )

    if challenger.rank < challenged.rank or challenger.rank - challenged.rank > 3:
        raise ValidationError(
            f"This challenger can only challenge teams with ranks "
            f"{max(1, challenger.rank - 3)} to {challenger.rank - 1}"
        )
        
    challenges1 = Challenge.objects.filter(challenger=challenger, challenge_date=challenge_date).exists()
    if challenges1:
        raise ValidationError('Challenger team already have Challenge on this date')
    
    challenges2 = Challenge.objects.filter(challenged=challenged, challenge_date=challenge_date).exists()
    if challenges2 :
        raise ValidationError('Challenged team already have Challenge on this date')

    today = date.today()
    if challenge_date == today:
        challenge_status = ChallengeStatus.TODAY
    elif challenge_date < today:
        challenge_status = ChallengeStatus.PENDING_RESULT
    else:
        challenge_status = ChallengeStatus.UPCOMING

    challenge = Challenge.objects.create(challenger=challenger, challenged=challenged, status=challenge_status, **validated_data)
    return challenge

def get_challenges():
    return Challenge.objects.all()

def delete_challenge(user, challenge_id):
    challenge = get_challenge_by_id(challenge_id)

    if user.team == None or user.team.id != challenge.challenger.id:
        raise ValidationError(
            "Only challenger can delete his own challenge"
        )

    challenge.delete()

    # if user.team.id == challenge.challenger.team.id

def get_challenge_by_id(challenge_id):
    try:
        return Challenge.objects.select_related("challenger", "challenged").get(id=challenge_id)
    except Challenge.DoesNotExist:
        raise NotFound("Challenge does not exist")



@transaction.atomic
def update_challenge_result(validated_data, challenge_id):
    challenge = get_challenge_by_id(challenge_id)

    if challenge.status != ChallengeStatus.PENDING_RESULT:
        raise ValidationError(
            "Only challenges with PENDING_RESULT can be updated"
        )

    challenger_points = validated_data.get("challenger_points")
    challenged_points = validated_data.get("challenged_points")

    if challenger_points is None or challenged_points is None:
        raise ValidationError("Both team scores are required")

    # Determine winner
    if challenger_points > challenged_points:
        winner = Winner.CHALLENGER_TEAM
    elif challenger_points < challenged_points:
        winner = Winner.CHALLENGED_TEAM
    else:
        winner = Winner.DRAW

    challenge.challenger_points = challenger_points
    challenge.challenged_points = challenged_points
    challenge.winner = winner

    challenger_team = challenge.challenger
    challenged_team = challenge.challenged

    challenger_rank = challenger_team.rank
    challenged_rank = challenged_team.rank

    if winner == Winner.CHALLENGER_TEAM:

        # Move all teams between challenged_rank and challenger_rank down by 1
        Team.objects.filter(
            rank__gte=challenged_rank,
            rank__lt=challenger_rank
        ).update(rank=F("rank") + 1)

        # Challenger takes challenged team's rank
        challenger_team.rank = challenged_rank
        challenger_team.save(update_fields=["rank"])

    challenge.status = ChallengeStatus.COMPLETED
    challenge.save()

    challenge.challenger.refresh_from_db()
    challenge.challenged.refresh_from_db()

    return challenge
