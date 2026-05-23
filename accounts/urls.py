from django.urls import path

from .views import LoginUserView, RegisterUserView, UsersView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('users/', UsersView.as_view(), name='all_users'),
]
