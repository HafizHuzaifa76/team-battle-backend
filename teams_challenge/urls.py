

from django.urls import path

from teams_challenge.views import ChallengeListView


urlpatterns = [
    path('', ChallengeListView.as_view(), name='challenges')
]
