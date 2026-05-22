from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            ValueError('Email is missing')
        
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "ADMIN")

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):

    class Role(models.TextChoices):
        ADMIN = "Admin", "ADMIN"
        CAPTAIN = "CAPTAIN", "Captain"
        PLAYER = "PLAYER", "Player"
    
    name = models.CharField(max_length=40)

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PLAYER
    )

    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"