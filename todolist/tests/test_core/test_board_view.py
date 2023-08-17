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


@pytest.mark.django_db()
class TestBoardView:

    def test_board_create(self, auth_client):
        url = '/goals/board/create'
        data = BoardFactory.build()
        response = auth_client.post(url, data=data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_board_unlogin_create(self, client):
        url = '/goals/board/create'
        data = BoardFactory.build()
        response = client.post(url, data=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_board_list(self, auth_client):
        url = '/goals/board/list'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK

