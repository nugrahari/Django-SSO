import pytest
from conftest import *


@pytest.mark.django_db
def test_login(client, test_user):
    assert test_user.check_password('password')
    response = client.post('/v1/auth/api/token/', {'username': 'testuser', 'password': 'password'})
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_and_access_api(client, test_user):
    response = client.get('/v1/user/api/')
    assert response.status_code == 401

    response = client.post('/v1/auth/api/token/', {'username': 'testuser', 'password': 'password'})
    token = response.json().get('access')
    assert token is not None

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = client.get('/v1/user/api/', headers=headers)
    assert response.status_code == 200


@pytest.mark.django_db
def test_logout(client, test_user):
    response = client.post('/v1/auth/api/token/', {'username': 'testuser', 'password': 'password'})
    token = response.json().get('access')
    assert token is not None

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = client.get('/v1/user/api/', headers=headers)
    assert response.status_code == 200

    response = client.post('/v1/auth/api/token/logout/', headers=headers)
    assert response.status_code == 200

    response = client.get('/v1/user/api/', headers=headers)
    assert response.status_code == 401
