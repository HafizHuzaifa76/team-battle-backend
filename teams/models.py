from email.policy import default
from random import choices
from django.db import models

class Category(models.TextChoices):
    PLATINUM = 'Platinum', 'PLATINUM'
    GOLD = 'Gold', 'GOLD'
    SILVER = 'Silver', 'SILVER'
    BRONZE = 'Bronze', 'BRONZE'

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100, default='Unknown Team')
    identifier = models.CharField(max_length=100, default='unknown_team')
    category = models.CharField(max_length = 30, choices = Category.choices, default = Category.BRONZE)
    rank = models.IntegerField()