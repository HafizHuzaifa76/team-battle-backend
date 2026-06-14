from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

from teams.basic_serializers import TeamBasicSerializer
from teams.models import Team

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is missing")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", Role.ADMIN)

        return self.create_user(email, password, **extra_fields)


class Role(models.TextChoices):
    ADMIN = "Admin", "ADMIN"
    CAPTAIN = "CAPTAIN", "Captain"
    PLAYER = "PLAYER", "Player"


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length = 100, default = 'New Player')
    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PLAYER
    )
    
    # age = models.IntegerField(
    #     null=True,
    #     blank=True
    # )

    team = models.ForeignKey(
        Team,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    def to_json(self):
        team = TeamBasicSerializer(self.team) if self.team else None
        data = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "team": team.data if self.team else None,
        }
        
        return data