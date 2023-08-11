# from pytest_factoryboy import register
# from factories import UserFactory
#
# pytest_plugins = "tests.fixtures"
#
# register(UserFactory)
# # register(CategoryFactory)
# # register(AdFactory)

# import pytest
# from pytest_factoryboy import register
# from django.test import Client

# from .factories import UserFactory

# # Factories
# register(UserFactory)
# register(BoardFactory)
# register(BoardParticipantFactory)
# register(CategoryFactory)
# register(GoalFactory)


# @pytest.fixture
# @pytest.mark.django_db
# def authenticated_user():
#     user = UserFactory.create()
#     password = user.password
#     user.set_password(password)
#     user.save()
#     client = Client()
#     client.login(username=user.username, password=password)
#     return {'client': client, 'user': user, 'password': password}