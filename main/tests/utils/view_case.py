from rest_framework.test import APIRequestFactory, APIClient
from main.tests.utils.base_case import BaseTestCase


class ViewTestCase(BaseTestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.factory = APIRequestFactory()
        super().setUpTestData()

    @classmethod
    def create_client(cls, **kwargs):
        client = APIClient()
        if 'token' in kwargs.keys():
            client.credentials(HTTP_AUTHORIZATION='Token ' + kwargs['token'])
        elif 'auth_user' in kwargs.keys():
            client.force_authenticate(kwargs['auth_user'])
        return client

    @classmethod
    def post(cls, endpoint, data=None, **kwargs):
        return cls.create_client(**kwargs).post(endpoint, data=data, format='json')

    @classmethod
    def put(cls, endpoint, data=None, **kwargs):
        return cls.create_client(**kwargs).put(endpoint, data=data, format='json')

    @classmethod
    def get(cls, endpoint, data=None, **kwargs):
        return cls.create_client(**kwargs).get(endpoint, data=data, format='json')
