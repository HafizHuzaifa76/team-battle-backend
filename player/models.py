from email.policy import default
from django.db import models

from accounts.models import Role
from teams.models import Team

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length = 100, default = 'New Player')
    age = models.IntegerField()
    email = models.EmailField()
    role = models.CharField(
        max_length=50,
        choices=Role.choices,
        default=Role.PLAYER
    )
    team = models.ForeignKey(
        Team,
        null=True,
        blank=True,
        related_name="players",
        on_delete=models.SET_NULL,
    )
