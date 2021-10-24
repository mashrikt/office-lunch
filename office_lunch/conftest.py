import pytest
from rest_framework.test import APIClient

from .restaurants.tests.factories import RestaurantFactory, MenuFactory
from .users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def staff_user():
    return UserFactory(is_staff=True)


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def auth_client(user, client):
    client.force_authenticate(user)
    return client


@pytest.fixture
def staff_auth_client(staff_user, client):
    client.force_authenticate(staff_user)
    return client


@pytest.fixture
def restaurant():
    return RestaurantFactory()


@pytest.fixture
def menu():
    return MenuFactory()
