

from teams.models import Team


def create_team(validated_data):
    last_team = Team.objects.order_by('-rank').first()

    next_rank = 1
    if last_team:
        next_rank = last_team.rank + 1

    team = Team.objects.create(
        name=validated_data['name'],
        rank=next_rank
    )

    return team

def get_all_teams():
    teams = Team.objects.all()

    return teams