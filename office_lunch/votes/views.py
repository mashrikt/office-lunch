from datetime import datetime

from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Vote, Winner
from .serializers import VoteSerializer, WinnerSerializer
from ..restaurants.permissions import IsAdminUserOrReadOnly


class VoteCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    filter_fields = ('menu__date',)

    def get_queryset(self):
        return Vote.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WinnerListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]
    queryset = Winner.objects.all()
    serializer_class = WinnerSerializer
    filter_fields = ('date',)

    def perform_create(self, instance):
        instance.save(date=datetime.today().date())
