

from django.shortcuts import get_object_or_404
from teams.models import Team
from teams_challenge.models import Challenge
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
        
    challenges1 = Challenge.objects.filter(challenger=challenger, challenge_date=challenge_date).exists()
    if challenges1:
        raise ValidationError('Challenger team already have Challenge on this date')
    
    challenges2 = Challenge.objects.filter(challenged=challenged, challenge_date=challenge_date).exists()
    if challenges2 :
        raise ValidationError('Challenged team already have Challenge on this date')

    validated_data['challenger'] = challenger
    validated_data['challenged'] = challenged

    challenge = Challenge.objects.create(**validated_data)
    return challenge

def get_challenges():
    return Challenge.objects.all()

def get_challenge_by_id(challenge_id):
    try:
        return Challenge.objects.get(id=challenge_id)
    except Challenge.DoesNotExist:
        raise NotFound('Challenge Not Exist')