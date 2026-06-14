from django.urls import path

from accounts.player_views import PlayerrDetailView, PlayersListView

urlpatterns = [
    path('', PlayersListView.as_view(), name='players'),
    path('<int:id>/', PlayerrDetailView.as_view(), name='player-by-id'),
]