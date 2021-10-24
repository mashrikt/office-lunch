from datetime import datetime

import factory
from faker import Faker

from ..models import Restaurant, Menu

fake = Faker()


class RestaurantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Restaurant
    name = factory.Faker('company')


class MenuFactory(factory.django.DjangoModelFactory):
    restaurant = factory.SubFactory(RestaurantFactory)
    date = datetime.now().date()
    cuisine = factory.Faker('word')
    items = factory.Faker('text')

    class Meta:
        model = Menu
