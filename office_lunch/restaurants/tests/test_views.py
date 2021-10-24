import factory
import pytest
from django.urls import reverse

from .factories import RestaurantFactory, MenuFactory
from ..models import Restaurant, Menu


class TestCreateRestaurant:

    @pytest.fixture
    def url(self):
        return reverse('api:restaurants:list_create')

    @pytest.fixture
    def restaurant_data(self):
        return factory.build(dict, FACTORY_CLASS=RestaurantFactory)

    def test_regular_user_cannot_create_restaurant(self, url, auth_client, restaurant_data):
        response = auth_client.post(url, data=restaurant_data)
        assert response.status_code == 403
        restaurant_exists = Restaurant.objects.filter(name__exact=restaurant_data['name']).exists()
        assert restaurant_exists is False

    def test_staff_user_can_create_restaurant(self, url, staff_auth_client, restaurant_data):
        response = staff_auth_client.post(url, data=restaurant_data)
        assert response.status_code == 201
        restaurant_exists = Restaurant.objects.filter(name__exact=restaurant_data['name']).exists()
        assert restaurant_exists is True


class TestUpdateRestaurant:

    @pytest.fixture
    def url(self, restaurant):
        return reverse('api:restaurants:retrieve_update', kwargs={'pk': restaurant.id})

    def test_regular_user_cannot_update_restaurant(self, url, restaurant, auth_client):
        response = auth_client.patch(url, data={'name': 'Burger King'})
        assert response.status_code == 403
        existing_restaurant = Restaurant.objects.get(id=restaurant.id)
        assert existing_restaurant.name != 'Burger King'

    def test_staff_user_can_update_restaurant(self, url, restaurant, staff_auth_client):
        response = staff_auth_client.patch(url, data={'name': 'Burger King'})
        assert response.status_code == 200
        existing_restaurant = Restaurant.objects.get(id=restaurant.id)
        assert existing_restaurant.name == 'Burger King'


class TestCreateMenu:

    @pytest.fixture
    def url(self):
        return reverse('api:menus:list_create')

    @pytest.fixture
    def menu_data(self, restaurant):
        menu_data = factory.build(dict, FACTORY_CLASS=MenuFactory)
        menu_data['restaurant'] = restaurant.id
        return menu_data

    def test_regular_user_cannot_create_menu(self, url, auth_client, menu_data):
        response = auth_client.post(url, data=menu_data)
        assert response.status_code == 403
        menu_exists = Menu.objects.filter(date=menu_data['date'], restaurant=menu_data['restaurant']).exists()
        assert menu_exists is False

    def test_staff_user_can_create_user(self, url, staff_auth_client, menu_data):
        response = staff_auth_client.post(url, data=menu_data)
        print("\n\n\n\n\n", menu_data)
        assert response.status_code == 201
        menu_exists = Menu.objects.filter(date=menu_data['date'], restaurant=menu_data['restaurant']).exists()
        assert menu_exists is True


class TestUpdateMenu:

    @pytest.fixture
    def url(self, menu):
        return reverse('api:menus:retrieve_update', kwargs={'pk': menu.id})

    def test_regular_user_cannot_update_menu(self, url, menu, auth_client):
        response = auth_client.patch(url, data={'cuisine': 'Bangladeshi'})
        assert response.status_code == 403
        existing_menu = Menu.objects.get(id=menu.id)
        assert existing_menu.cuisine != 'Bangladeshi'

    def test_staff_user_can_update_menu(self, url, menu, staff_auth_client):
        response = staff_auth_client.patch(url, data={'cuisine': 'Bangladeshi'})
        assert response.status_code == 200
        existing_menu = Menu.objects.get(id=menu.id)
        assert existing_menu.cuisine == 'Bangladeshi'

    def test_regular_user_cannot_delete_menu(self, url, menu, auth_client):
        response = auth_client.delete(url)
        assert response.status_code == 403
        menu_exists = Menu.objects.filter(id=menu.id).exists()
        assert menu_exists is True

    def test_staff_user_can_delete_menu(self, url, menu, staff_auth_client):
        response = staff_auth_client.delete(url)
        assert response.status_code == 204
        menu_exists = Menu.objects.filter(id=menu.id).exists()
        assert menu_exists is False
