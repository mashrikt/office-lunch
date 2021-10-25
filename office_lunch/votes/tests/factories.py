from datetime import datetime

import factory
from faker import Faker

from ..models import Vote, Winner
from ...restaurants.tests.factories import MenuFactory
from ...users.tests.factories import UserFactory

fake = Faker()


class VoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vote

    menu = factory.SubFactory(MenuFactory)
    user = factory.SubFactory(UserFactory)


class WinnerFactory(factory.django.DjangoModelFactory):
    menu = factory.SubFactory(MenuFactory)
    vote_count = factory.Faker('random_int')
    date = datetime.now().date()

    class Meta:
        model = Winner
