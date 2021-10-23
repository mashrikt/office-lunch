import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from .factories import fake


class TestCreateUser:

    @pytest.fixture
    def url(self):
        return reverse('api:users:list_create')

    @pytest.fixture
    def register_data(self):
        data = {
            'username': fake.user_name(),
            'password': '0ffice-Lunch'
        }
        return data

    def test_regular_user_cannot_create_user(self, url, auth_client, register_data):
        response = auth_client.post(url, data=register_data)
        assert response.status_code == 403
        user_exists = User.objects.filter(username__exact=register_data['username']).exists()
        assert user_exists is False

    def test_staff_user_can_create_user(self, url, staff_auth_client, register_data):
        response = staff_auth_client.post(url, data=register_data)
        assert response.status_code == 201
        user_exists = User.objects.filter(username__exact=register_data['username']).exists()
        assert user_exists is True


class TestUpdateUser:

    @pytest.fixture
    def url(self, user):
        return reverse('api:users:retrieve_update', kwargs={'pk': user.id})

    def test_regular_user_cannot_update_user(self, url, user, auth_client):
        response = auth_client.patch(url, data={'is_staff': True})
        assert response.status_code == 403
        user = User.objects.get(id=user.id)
        assert user.is_staff is False

    def test_staff_user_can_update_user(self, url, user, staff_auth_client):
        response = staff_auth_client.patch(url, data={'is_staff': True})
        assert response.status_code == 200
        user = User.objects.get(id=user.id)
        assert user.is_staff is True
