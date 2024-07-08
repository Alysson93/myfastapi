from http import HTTPStatus

from schemas import UserResponse


def test_root(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'msg': 'Hello, World!'}


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


def test_create_user_already_exists(client, user):
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
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


def test_read_user_by_id(client, user):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'JohnDoe',
        'name': 'John Doe',
        'email': 'john@test.com',
        'phone': '81912345678',
    }


def test_read_user_by_id_not_found(client):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_read_users_with_user(client, user):
    response = client.get('/users/')
    user_response = UserResponse.model_validate(user).model_dump()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [user_response]


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'JaneDoe',
            'password': '456',
            'name': 'Jane Doe',
            'email': 'jane@test.com',
            'phone': '00912345678',
        },
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_update_user_not_found(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'JaneDoe',
            'password': '456',
            'name': 'Jane Doe',
            'email': 'jane@test.com',
            'phone': '00912345678',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client, user):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_user_not_found(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.NOT_FOUND
