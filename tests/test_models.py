from sqlalchemy import select

from models import User


def test_user(session):
    user = User(
        username='JohnDoe',
        password='123',
        name='John Doe',
        email='john@test.com',
        phone='81912345678',
    )
    session.add(user)
    session.commit()
    result = session.scalar(select(User).where(User.id == 1))
    assert result.email == 'john@test.com'
