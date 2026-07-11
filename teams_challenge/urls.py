from django.urls import path
from teams_challenge.views import ChallengeCronView, ChallengeDetaiView, ChallengeListView, ChallengeResultView, MyChallengesView


urlpatterns = [
    path('', ChallengeListView.as_view(), name='challenges'),
    path('my-challenges/', MyChallengesView.as_view(), name='my-challenges'),
    path('<int:challenge_id>/', ChallengeDetaiView.as_view(), name='challenges-by-id'),
    path('result/<int:challenge_id>/', ChallengeResultView.as_view(), name='challenges-result'),
    path('cron/update-statuses', ChallengeCronView.as_view(), name='challenges-status-update')
]
