import pytest
from rest_framework import status


# from ..factories import UserFactory


# @pytest.mark.django_db
# def test_user_data(client):
#     user_data = UserFactory.create_batch(4)
#     response = client.get("/ads/")
#     assert response.status_code == status.HTTP_200_OK
    # assert response.data == {
    #     "count": 4,
    #     "next": None,
    #     "previous": None,
    #     "results": AdListSerializer(ad_list, many=True).data
    # }