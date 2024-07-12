from jwt import decode

from security import ALGORITHM, SECRET_KEY, create_access_token


def test_jwt():
    token = create_access_token({'sub': 'test@test.com'})
    result = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert result['sub'] == 'test@test.com'
    assert result['exp']
