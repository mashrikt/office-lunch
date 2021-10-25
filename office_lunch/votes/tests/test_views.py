from datetime import datetime

import pytest
from django.urls import reverse

from .factories import VoteFactory, WinnerFactory
from ..models import Vote, Winner
from ..utils import get_last_n_working_days
from ...restaurants.tests.factories import MenuFactory


class TestCreateVote:

    @pytest.fixture
    def url(self):
        return reverse('api:votes:create')

    def test_user_can_vote(self, url, auth_client, menu, user):
        data = {'menu': menu.id}
        response = auth_client.post(url, data=data)
        assert response.status_code == 201
        vote_exists = Vote.objects.filter(menu=menu, user=user).exists()
        assert vote_exists is True

    def test_user_cannot_vote_twice(self, url, auth_client, menu, user):
        VoteFactory(user=user)
        data = {'menu': menu.id}
        response = auth_client.post(url, data=data)
        assert response.status_code == 400
        assert response.json()['non_field_errors'] == ['User has already voted!']
        vote_exists = Vote.objects.filter(menu=menu, user=user).exists()
        assert vote_exists is False

    def test_user_cannot_vote_for_past_menu(self, url, auth_client, user):
        last_day = get_last_n_working_days(1)[0]
        menu = MenuFactory(date=last_day)
        data = {'menu': menu.id}
        response = auth_client.post(url, data=data)
        assert response.status_code == 400
        assert response.json()['non_field_errors'] == ['User cannot vote for past dates!']
        vote_exists = Vote.objects.filter(menu=menu, user=user).exists()
        assert vote_exists is False

    def test_user_cannot_vote_after_winner_determined(self, url, auth_client, user, winner):
        data = {'menu': winner.menu.id}
        response = auth_client.post(url, data=data)
        assert response.status_code == 400
        assert response.json()['non_field_errors'] == ['Voting concluded for the day!']
        vote_exists = Vote.objects.filter(menu=winner.menu, user=user).exists()
        assert vote_exists is False


class TestListVote:

    @pytest.fixture
    def url(self):
        return reverse('api:votes:create')

    def test_user_see_their_vote(self, url, auth_client, user):
        vote = VoteFactory(user=user)
        response = auth_client.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]['menu']['id'] == vote.menu.id

    def test_returns_empty_when_user_hasnt_voted(self, url, auth_client):
        response = auth_client.get(url)
        assert response.status_code == 200
        assert response.json() == []

    def test_user_cant_see_anothers_votes(self, url, auth_client, vote):
        today = datetime.today().date()
        vote_exists = Vote.objects.filter(menu__date=today).exists()
        response = auth_client.get(url)
        assert vote_exists is True
        assert response.status_code == 200
        assert response.json() == []


class TestCreateWinner:

    @pytest.fixture
    def url(self):
        return reverse('api:winners:list-create')

    def test_regular_user_cannot_generate_winner(self, url, auth_client, vote):
        response = auth_client.post(url)
        assert response.status_code == 403

    def test_generate_winner(self, url, staff_auth_client, vote):
        today = datetime.today().date()
        response = staff_auth_client.post(url)
        assert response.status_code == 201
        is_winner_generated = Winner.objects.filter(date=today, menu=vote.menu, vote_count=1).exists()
        assert is_winner_generated is True

    def test_once_winner_generated_cannot_generate_again(self, url, staff_auth_client, winner):
        response = staff_auth_client.post(url)
        assert response.status_code == 400
        assert response.json()['non_field_errors'] == ['Winner already exists!']

    def test_restaurant_wins_twice_in_a_row(self, url, staff_auth_client, restaurant):
        # create last days's winner
        last_day = get_last_n_working_days(1)[0]
        last_days_mennu = MenuFactory(restaurant=restaurant, date=last_day)
        WinnerFactory(menu=last_days_mennu, date=last_day)

        # create today's vote
        todays_menu = MenuFactory(restaurant=restaurant)
        VoteFactory(menu=todays_menu)

        response = staff_auth_client.post(url)
        assert response.status_code == 201
        assert response.json()['menu']['restaurant']['id'] == restaurant.id
        last_day_winner_exists = Winner.objects.filter(date=last_day, menu__restaurant=restaurant).exists()
        assert last_day_winner_exists is True
        today_winner_exists = Winner.objects.filter(date=last_day, menu__restaurant=restaurant).exists()
        assert today_winner_exists is True

    def test_restaurant_won_previous_two_not_winner_today(self, url, staff_auth_client, restaurant):
        """
        if there's only votes for the twice recurring winner restaurant in the 3rd day, no winner will be
        determined.
        """
        # created last day's winner
        last_day = get_last_n_working_days(1)[0]
        last_days_mennu = MenuFactory(restaurant=restaurant, date=last_day)
        WinnerFactory(menu=last_days_mennu, date=last_day)

        # created second last days winner
        second_last_day = get_last_n_working_days(2)[0]
        second_last_days_mennu = MenuFactory(restaurant=restaurant, date=second_last_day)
        WinnerFactory(menu=second_last_days_mennu, date=second_last_day)

        todays_menu = MenuFactory(restaurant=restaurant)
        VoteFactory(menu=todays_menu)
        response = staff_auth_client.post(url)
        assert response.status_code == 400
        assert response.json() == ['Cannot generate a winner!']

    def test_restaurant_won_previous_two_another_restaurant_wins_today(self, url, staff_auth_client, restaurant):
        """
        even if twice recurring winner has more votes, it won't be the winner on the third day, menu with the second
        highest vote will win
        """
        # created last day's winner
        last_day = get_last_n_working_days(1)[0]
        last_days_mennu = MenuFactory(restaurant=restaurant, date=last_day)
        WinnerFactory(menu=last_days_mennu, date=last_day)

        # created second last days winner
        second_last_day = get_last_n_working_days(2)[0]
        second_last_days_mennu = MenuFactory(restaurant=restaurant, date=second_last_day)
        WinnerFactory(menu=second_last_days_mennu, date=second_last_day)

        # restaurant that won last 2 days, has 2 votes, another restaurant has 1 vote
        todays_menu = MenuFactory(restaurant=restaurant)
        another_restaurant_menu = MenuFactory()
        VoteFactory(menu=todays_menu)
        VoteFactory(menu=todays_menu)
        VoteFactory(menu=another_restaurant_menu)

        response = staff_auth_client.post(url)
        assert response.status_code == 201
        assert response.json()['menu']['restaurant']['id'] == another_restaurant_menu.restaurant.id
        today = datetime.today().date()
        is_another_restaurant_winner_today = Winner.objects.filter(menu=another_restaurant_menu, date=today).exists()
        assert is_another_restaurant_winner_today is True
        is_recurring_winner_winner_today = Winner.objects.filter(menu=todays_menu, date=today).exists()
        assert is_recurring_winner_winner_today is False

    def test_two_restaurant_same_vote(self, url, staff_auth_client):
        """
        When two restaurants have the same highest votes, one of them elected winner.
        """

        menu_1 = MenuFactory()
        menu_2 = MenuFactory()

        VoteFactory(menu=menu_1)
        VoteFactory(menu=menu_2)

        response = staff_auth_client.post(url)
        assert response.status_code == 201
        assert response.json()['menu']['restaurant']['id'] in [menu_1.restaurant.id, menu_2.restaurant.id]


class TestListWinner:

    @pytest.fixture
    def url(self):
        return reverse('api:winners:list-create')

    def test_user_can_see_todays_winner(self, url, auth_client, winner):
        today = datetime.today().date().strftime('%Y-%m-%d')
        response = auth_client.get(url, {'date': today})
        assert response.status_code == 200
        assert response.json()[0]['date'] == today
        assert response.json()[0]['menu']['id'] == winner.menu.id

    def test_when_no_winner_determined_returns_empty(self, url, auth_client):
        today = datetime.today().date().strftime('%Y-%m-%d')
        response = auth_client.get(url, {'date': today})
        assert response.status_code == 200
        assert response.json() == []
