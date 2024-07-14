from jwt import decode

from security import settings, create_access_token


def test_jwt():
    token = create_access_token({'sub': 'test@test.com'})
    result = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    assert result['sub'] == 'test@test.com'
    assert result['exp']
