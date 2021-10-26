from django.urls import path

from .views import VoteCreateAPIView, WinnerListCreateAPIView

vote_urlpatterns = [
    path('', VoteCreateAPIView.as_view(), name='create'),
]


winner_urlpatterns = [
    path('', WinnerListCreateAPIView.as_view(), name='list-create'),
]
