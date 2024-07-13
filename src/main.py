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
from security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

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
    limit: int = 10,
    offset: int = 0,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return users


@app.get('/users/{id:int}', response_model=UserResponse)
def read_user_by_id(
    id: int,
    current_user=Depends(get_current_user),
):
    if current_user.id != id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Not enough permission'
        )
    return current_user


@app.put('/users/{id:int}', status_code=HTTPStatus.NO_CONTENT)
def update_user(
    id: int,
    user: UserRequest,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if current_user.id != id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Not enough permission'
        )
    current_user.username = user.username
    current_user.password = get_password_hash(user.password)
    current_user.name = user.name
    current_user.email = user.email
    current_user.phone = user.phone
    session.commit()


@app.delete('/users/{id:int}', status_code=HTTPStatus.NO_CONTENT)
def delete_user(
    id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if current_user.id != id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Not enough permission'
        )
    session.delete(current_user)
    session.commit()


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
