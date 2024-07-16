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
