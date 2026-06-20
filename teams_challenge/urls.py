from django.urls import path
from teams_challenge.views import ChallengeDetaiView, ChallengeListView, ChallengeResultView


urlpatterns = [
    path('', ChallengeListView.as_view(), name='challenges'),
    path('<int:challenge_id>/', ChallengeDetaiView.as_view(), name='challenges'),
    path('result/<int:challenge_id>/', ChallengeResultView.as_view(), name='challenges')
]
