from django.utils import timezone
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Vote, Winner
from .serializers import VoteSerializer, WinnerSerializer
from ..restaurants.permissions import IsAdminUserOrReadOnly


class VoteCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListCreateWinnerAPIView(ListCreateAPIView):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Winner.objects.all()
    serializer_class = WinnerSerializer
    filter_fields = ('date',)

    def perform_create(self, instance):
        instance.save(date=timezone.now().date())
