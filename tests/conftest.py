import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../src')

import factory
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from db import get_session
from main import app
from models import User, table_registry
from security import get_password_hash


@fixture()
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    table_registry.metadata.drop_all(engine)


@fixture()
def client(session):
    def fake_session():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = fake_session
        yield client
    app.dependency_overrides.clear()


@fixture()
def user(session):
    user = UserFactory(password=get_password_hash('123'))
    session.add(user)
    session.commit()
    session.refresh(user)
    user.clean_password = '123'
    return user


@fixture
def other_user(session):
    user = UserFactory(password=get_password_hash('123'))
    session.add(user)
    session.commit()
    session.refresh(user)
    user.clean_password = '123'
    return user


@fixture
def token(client, user):
    response = client.post(
        '/auth/token/', data={'username': user.username, 'password': '123'}
    )
    return response.json()['access_token']


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    password = factory.LazyAttribute(lambda obj: f'pass{obj.username}')
    name = factory.LazyAttribute(lambda obj: f'name{obj.username}')
    email = factory.Sequence(lambda n: f'{n}@test.com')
    phone = factory.LazyAttribute(lambda obj: f'(11){obj.username}')
