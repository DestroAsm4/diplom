import factory
import pytest
from django.contrib.auth import get_user
from rest_framework import status

from core.models import User


class LoginRequestFactory(factory.DictFactory):
    username = factory.Faker('user_name')
    password = factory.Faker('password')


class BoardFactory(factory.DictFactory):
    id = factory.Faker('random_int')
    title = factory.Faker('word')
    is_deleted = False


class GoalFactory(factory.DictFactory):
    title = factory.Faker('word')
    is_deleted = False
    board = BoardFactory.build().get('id')


@pytest.mark.django_db()
class TestGoalView:

    def test_goal_list(self, auth_client):
        url = '/goals/goal/list'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK