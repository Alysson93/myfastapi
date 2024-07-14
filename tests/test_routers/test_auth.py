from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        '/auth/token/', data={'username': user.username, 'password': '123'}
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert token['access_token']
