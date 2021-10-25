from django.urls import path, include

from .views import VoteCreateAPIView, ListCreateWinnerAPIView

vote_urlpatterns = [
    path('', VoteCreateAPIView.as_view(), name='create'),
]


winner_urlpatterns = [
    path('', ListCreateWinnerAPIView.as_view(), name='list-create'),
]
