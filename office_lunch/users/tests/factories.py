import factory
from django.contrib.auth.models import User
from faker import Faker


fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', '0ffice-Lunch')
    is_staff = False
