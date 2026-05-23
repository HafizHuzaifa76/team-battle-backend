from django.urls import path

from teams.views import TeamListView


urlpatterns = [
    path('', TeamListView.as_view(), name='team'),
]
