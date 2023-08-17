import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .factories import UserFactory

register(UserFactory)


@pytest.fixture()
def client() -> APIClient:
    """Rest Framework test client instance."""
    return APIClient()


@pytest.fixture()
def auth_client(client, user):
    """Authenticated Rest Framework client"""
    client.force_login(user)
    return client