import factory
import pytest
from django.contrib.auth import get_user
from rest_framework import status

from core.models import User


class LoginRequestFactory(factory.DictFactory):
    username = factory.Faker('user_name')
    password = factory.Faker('password')



@pytest.mark.django_db()
class TestLoginView:
    url = '/core/login'

    def test_user_does_not_exists(self, client):
        data = LoginRequestFactory.create()
        response = client.post(self.url, data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_invalid_password(self, client, user):
        data = LoginRequestFactory.create(username=user.username)
        response = client.post(self.url, data=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_session_creates_on_login(self, client, user_factory):
        data = LoginRequestFactory.create()
        user = user_factory.create(username=data['username'], password=data['password'])

        response = client.post(self.url, data=data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == self._serialize_response(user)
        assert get_user(client).is_authenticated

    @staticmethod
    def _serialize_response(user: User, **kwargs) -> dict:
        data = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.last_name,
        }
        data |= kwargs
        return data