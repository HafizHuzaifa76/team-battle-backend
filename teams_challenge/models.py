from random import choices
from django.db import models

from teams.models import Team

class Winner(models.TextChoices):
    CHALLENGER_TEAM = 'CHALLENGER_TEAM', 'Challenger_Team'
    CHALLENGED_TEAM = 'CHALLENGED_TEAM', 'Challenged_Team'
    DRAW = 'DRAW', 'Draw'


# Create your models here.
class Challenge(models.Model):
    challenger = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="challenges_initiated",
    )

    challenged = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="challenges_received",
    )

    challenge_date = models.DateField()

    winner = models.CharField(
        max_length=20,
        choices=Winner.choices,
        null=True,
        blank=True,
    )

    challenger_points = models.PositiveIntegerField(null=True, blank=True)
    challenged_points = models.PositiveIntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-challenge_date"]

    def __str__(self):
        return f"{self.challenger} vs {self.challenged} ({self.challenge_date})"