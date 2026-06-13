

from django.shortcuts import get_object_or_404
from django.utils.ipv6 import ValidationError
from teams_challenge.models import Challenge


def create_challenge(validated_data):
    challenger_team = validated_data.get('challenger')
    challenged_team = validated_data.get('challenged')
    challenge_date = validated_data.get('challenge_date')

    if(challenger_team == challenged_team):
        raise ValidationError(
            message='Team cannot challenge itself'
        )
        
    challenges1 = Challenge.objects.get(challenger=challenger_team, challenge_date=challenge_date)
    if not challenges1 == None :
        raise ValidationError(message='Challenger team already have Challenge on this date')
    
    challenges2 = Challenge.objects.get(challenged=challenged_team, challenge_date=challenge_date)
    if not challenges2 == None :
        raise ValidationError(message='Challenged team already have Challenge on this date')
    
    challenge = Challenge.objects.create(validated_data)
    return challenge

def get_challenges():
    return Challenge.objects.all()