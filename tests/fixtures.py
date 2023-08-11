import pytest


@pytest.fixture
@pytest.mark.django_db
def create_user_fix(client, django_user_model):
    username = 'test'
    password = 'qwe123'
    django_user_model.objects.create(username=username, password=password)
    response = client.post('/signup', data={"username": username, 'password': password})
    return response.data
# #
# #
# @pytest.fixture
# @pytest.mark.django_db
# def user_with_access_token(client, django_user_model):
#     username = 'test'
#     password = 'qwe123'
#     user = django_user_model.objects.create(username=username, password=password)
#     response = client.post('/users/token/', data={"username": username, 'password': password})
#     return user, response.data.get('access')