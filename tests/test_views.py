import pytest
# from django.contrib.auth.models import User
from django.test import Client

from todolist.core.models import User


@pytest.mark.django_db
class TestUserLoginAuthentication:
    """
    Test user signup
    """

    def test_user_signup(self):
        client = Client()
        response = client.post(
            '/core/signup',
            {'username': 'test_user', 'password': 'Qwe123!', 'password_repeat': 'Qwe123!'}
        )
        expected_response = {'id': 1, 'username': 'test_user', 'email': '', 'first_name': '', 'last_name': ''}
        assert response.status_code == 201
        assert response.data == expected_response

    def test_user_login(self, authenticated_user: dict):
        """
        Test user login
        """
        client = authenticated_user.get('client')
        user = authenticated_user.get('user')
        password = authenticated_user.get('password')

        response = client.post(
            '/core/login',
            {'username': user.username, 'password': password},
            content_type='application/json',
        )
        expected_response = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        assert response.status_code == 200
        assert response.data == expected_response

    def test_core_profile(self, authenticated_user: dict):
        """
        Test for user profile retrieval, update, patch (with validation error for username)
        """
        client = authenticated_user.get('client')
        user = authenticated_user.get('user')

        response = client.get('/core/profile')
        expected_response = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        assert response.status_code == 200
        assert response.data == expected_response

        changed_data = {
            'username': 'new_name',
            'email': 'new_test@test.com',
            'first_name': 'new_name',
            'last_name': 'new_surname',
        }

        # Test PUT method
        response = client.put('/core/profile', changed_data)
        changed_data['id'] = user.id

        assert response.status_code == 200
        assert response.data == changed_data

        # Test PATCH method with username already exists
        User.objects.create(username='user_exists', password='testPassword')
        response = client.patch('/core/profile', {'username': 'user_exists'})

        assert response.status_code == 400
        assert 'username already exists' in response.data.get('username')[0]

    def test_core_update_password(self, authenticated_user: dict):
        """
        Test user update password
        """
        client = authenticated_user.get('client')
        password = authenticated_user.get('password')

        response = client.put(
            '/core/update_password',
            {'old_password': password, 'new_password': 'new_Password1234'}
        )
        assert response.status_code == 200
        assert response.data == {}


@pytest.mark.django_db
class TestBoards:
    expected_fields = ['id', 'created', 'updated', 'title', 'is_deleted']

    def test_board_list(self, authenticated_user: dict):
        """
        Test user get boards list
        """
        client = authenticated_user.get('client')
        response = client.get('/goals/board/list')

        assert response.status_code == 200
        for field in self.expected_fields:
            assert field in response.data[0]

    def test_board_create_update_delete(self, authenticated_user: dict, users: list):
        """
        Test user create, update, delete a board
        """
        client = authenticated_user.get('client')
        user = authenticated_user.get('user')

        response = client.post(
            '/goals/board/create',
            {'title': 'New board'},
            content_type='application/json',
        )

        assert response.status_code == 201
        for field in self.expected_fields:
            assert field in response.data