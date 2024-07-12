import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../src')

from http import HTTPStatus

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import get_session
from models import User
from schemas import Token, UserRequest, UserResponse
from security import create_access_token, get_password_hash, verify_password, get_current_user

app = FastAPI()


@app.get('/')
def root():
    return {'msg': 'Hello, World!'}


@app.post(
    '/users/', status_code=HTTPStatus.CREATED, response_model=UserResponse
)
def create_user(user: UserRequest, session: Session = Depends(get_session)):
    result = session.scalar(
        select(User).where(
            User.username == user.username or User.email == user.email
        )
    )
    if result is None:
        new_user = User(
            username=user.username,
            password=get_password_hash(user.password),
            name=user.name,
            email=user.email,
            phone=user.phone,
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    else:
        raise (
            HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='User already exists',
            )
        )


@app.get('/users/', response_model=list[UserResponse])
def read_users(
    limit: int = 10, offset: int = 0, session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return users


@app.get('/users/{id:int}', response_model=UserResponse)
def read_user_by_id(id: int, session: Session = Depends(get_session)):
    user = session.scalar(select(User).where(User.id == id))
    if user:
        return user
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )


@app.put('/users/{id:int}', status_code=HTTPStatus.NO_CONTENT)
def update_user(
    id: int, user: UserRequest, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == id))
    if db_user:
        db_user.username = user.username
        db_user.password = get_password_hash(user.password)
        db_user.name = user.name
        db_user.email = user.email
        db_user.phone = user.phone
        session.commit()
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )


@app.delete('/users/{id:int}', status_code=HTTPStatus.NO_CONTENT)
def delete_user(id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == id))
    if db_user:
        session.delete(db_user)
        session.commit()
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )


@app.post('/token/', response_model=Token)
def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(
        select(User).where(User.username == form_data.username)
    )
    if user and verify_password(form_data.password, user.password):
        access_token = create_access_token({'sub': user.username})
        return {'access_token': access_token, 'token_type': 'Bearer'}
    else:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Invalid credentials'
        )


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
