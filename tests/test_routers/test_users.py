from http import HTTPStatus

from schemas import UserResponse


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'JohnDoe',
            'password': '123',
            'name': 'John Doe',
            'email': 'john@test.com',
            'phone': '00912345678',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'JohnDoe',
        'name': 'John Doe',
        'email': 'john@test.com',
        'phone': '00912345678',
    }


def test_create_user_already_exists_username(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'password': '123',
            'name': 'John Doe',
            'email': 'john@test.com',
            'phone': '00912345678',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_user_already_exists_email(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'JohnDoe',
            'password': '123',
            'name': 'John Doe',
            'email': user.email,
            'phone': '00912345678',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_read_users(client, user, token):
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )
    user_response = UserResponse.model_validate(user).model_dump()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [user_response]


def test_read_user_by_id(client, user, token):
    response = client.get(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    user_response = UserResponse.model_validate(user).model_dump()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_response
    assert response.status_code == HTTPStatus.OK


def test_read_user_by_id_not_found(client, token):
    response = client.get(
        '/users/2', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_update_user(client, token):
    response = client.put(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'JaneDoe',
            'password': '456',
            'name': 'Jane Doe',
            'email': 'jane@test.com',
            'phone': '00912345678',
        },
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_update_user_not_found(client, token):
    response = client.put(
        '/users/2',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'JaneDoe',
            'password': '456',
            'name': 'Jane Doe',
            'email': 'jane@test.com',
            'phone': '00912345678',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'JaneDoe',
            'password': '456',
            'name': 'Jane Doe',
            'email': 'jane@test.com',
            'phone': '00912345678',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_user(client, token):
    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_user_not_found(client, token):
    response = client.delete(
        '/users/2', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_user_with_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
