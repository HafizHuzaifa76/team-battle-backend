

from .models import User


def get_all_users():
    users = User.objects.all()
    return users
