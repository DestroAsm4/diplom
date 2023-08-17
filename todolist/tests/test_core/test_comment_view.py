import factory
import pytest
from django.contrib.auth import get_user
from rest_framework import status

from core.models import User


@pytest.mark.django_db()
class TestCommentView:

    def test_comment_list(self, auth_client):
        url = '/goals/goal_comment/list'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK