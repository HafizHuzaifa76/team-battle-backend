from django.urls import path

from teams.views import MyTeamView, TeamDetailView, TeamListView


urlpatterns = [
    path('', TeamListView.as_view(), name='team'),
    path('my-team/', MyTeamView.as_view(), name='team'),
    path('<int:id>/', TeamDetailView.as_view(), name='team-by-id'),
]
