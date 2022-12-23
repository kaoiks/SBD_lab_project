import pytest

from django.contrib.auth.models import User

from rest_framework.test import APIClient


@pytest.fixture
def client():
    client = APIClient()

    username = 'pytest-superuser'
    password = 'pytest-superuser'
    pytest_user = User.objects.create_superuser(username=username, password=password)
    data = {'username': username, 'password': password, 'email': pytest_user.email}

    response = client.post('/auth/login/', data=data)
    token = response.json().get('access')

    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    return client
