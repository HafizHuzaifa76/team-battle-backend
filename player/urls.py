from django.urls import path

from .views import PlayersListView



urlpatterns = [
    path('', PlayersListView.as_view(), name='players'),
]
