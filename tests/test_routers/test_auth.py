from http import HTTPStatus
from freezegun import freeze_time


def test_get_token(client, user):
    response = client.post(
        '/auth/token/', data={'username': user.username, 'password': '123'}
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert token['access_token']


def test_token_expires_after_time(client, user):
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/auth/token', data={'username': user.username, 'password': '123'}
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']
    with freeze_time('2023-07-14 12:31:00'):
        response = client.put(
            f'/users/{user.id}',
            json={
                'username': 'wrongwrong',
                'name': 'Wrong',
                'phone': '(xx)xxxxxxxx',
                'email': 'wrong@wrong.com',
                'password': 'wrong',
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Not authenticated'}


def test_token_inexistent_user(client):
    response = client.post(
        '/auth/token',
        data={'username': 'no_user@no_domain.com', 'password': 'testtest'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Invalid credentials'}


def test_token_wrong_password(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': 'testtest'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Invalid credentials'}


def test_token_wrong_username(client, user):
    response = client.post(
        '/auth/token',
        data={'username': 'WrongUser', 'password': user.password},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Invalid credentials'}


def test_refresh_token(client, token):
    response = client.post(
        '/auth/refresh-token',
        headers={'Authorization': f'Bearer {token}'},
    )
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


def test_token_expired_dont_refresh(client, user):
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.username, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.post(
            '/auth/refresh-token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
