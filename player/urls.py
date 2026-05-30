from django.urls import path

from .views import PlayerrDetailView, PlayersListView



urlpatterns = [
    path('', PlayersListView.as_view(), name='players'),
    path('<int:id>/', PlayerrDetailView.as_view(), name='player-by-id'),
]
