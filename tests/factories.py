import factory

from todolist.core.models import User
#
#
# # from ads.models import Ad, Categories
# # from users.models import User
#
#
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Faker('name')
    email = factory.Faker('email')

from factory import Faker
from factory.django import DjangoModelFactory

from todolist.core.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker('user_name')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')
    password = Faker('password')