from datetime import datetime

from django.db.models import Count
from rest_framework import serializers

from .models import Vote, Winner
from .utils import get_last_n_working_days
from ..restaurants.models import Menu
from ..restaurants.relations import PresentablePrimaryKeyRelatedField
from ..restaurants.serializers import MenuSerializer


class VoteSerializer(serializers.ModelSerializer):
    menu = PresentablePrimaryKeyRelatedField(
        queryset=Menu.objects.all(),
        presentation_serializer=MenuSerializer
    )

    class Meta:
        model = Vote
        fields = ['menu']

    def validate(self, data):
        user = self.context['request'].user
        menu = data['menu']
        already_voted = Vote.objects.filter(user=user, menu__date=menu.date)
        voting_concluded = Winner.objects.filter(menu__date=datetime.today().date())
        if menu.date < datetime.today().date():
            raise serializers.ValidationError('User cannot vote for past dates!')
        if already_voted:
            raise serializers.ValidationError('User has already voted!')
        if voting_concluded:
            raise serializers.ValidationError('Voting concluded for the day!')
        return data


class WinnerSerializer(serializers.ModelSerializer):
    menu = MenuSerializer(read_only=True)

    class Meta:
        model = Winner
        fields = ['id', 'date', 'menu', 'vote_count']
        read_only_fields = ['date', 'menu', 'vote_count']

    def validate(self, data):
        today = datetime.today().date()
        winner_exists = Winner.objects.filter(date=today)
        if winner_exists:
            raise serializers.ValidationError('Winner already exists!')
        return data

    def get_last_winner(self):
        return Winner.objects.filter(
            date__in=get_last_n_working_days(1)
        ).values_list(
            'menu__restaurant', flat=True
        )

    def get_twice_recurring_winner(self):
        return Winner.objects.filter(
            date__in=get_last_n_working_days(2),
            menu__restaurant__in=self.get_last_winner()
        ).values(
            'menu__restaurant'
        ).annotate(
            wins=Count('menu__restaurant')
        ).filter(
            wins=2
        ).values_list(
            'menu__restaurant', flat=True
        )

    def get_winning_restaurant(self):
        today = datetime.today().date()
        return Vote.objects.exclude(
            menu__restaurant_id__in=self.get_twice_recurring_winner(),
        ).filter(
            menu__date=today
        ).values(
            'menu_id',
        ).annotate(
            vote_count=Count('menu_id')
        ).latest(
            'vote_count'
        )

    def create(self, validated_data):
        try:
            winner_data = self.get_winning_restaurant()
        except Vote.DoesNotExist:
            raise serializers.ValidationError('Cannot generate a winner!')
        validated_data['menu_id'] = winner_data['menu_id']
        validated_data['vote_count'] = winner_data['vote_count']
        return Winner.objects.create(**validated_data)
