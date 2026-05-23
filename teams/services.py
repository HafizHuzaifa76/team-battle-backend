

from teams.models import Team


def create_team(validated_data):
    team = Team.objects.create(validated_data)

    return team

def get_all_teams():
    teams = Team.objects.all()

    return teams