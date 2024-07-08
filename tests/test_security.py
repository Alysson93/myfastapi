from jwt import decode

from security import ALGORITHM, SECRET_KEY, create_acess_token


def test_jwt():
    data = {'sub': 'test@test.com'}
    token = create_acess_token(data)
    result = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert result['sub'] == data['sub']
    assert result['exp']
