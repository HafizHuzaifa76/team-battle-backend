

from django.urls import path

from teams_challenge.views import ChallengeDetaiView, ChallengeListView


urlpatterns = [
    path('', ChallengeListView.as_view(), name='challenges'),
    path('<int:challenge_id>/', ChallengeDetaiView.as_view(), name='challenges')
]
