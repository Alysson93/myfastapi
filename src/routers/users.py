from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import get_session
from models import User
from schemas import UserRequest, UserResponse
from security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])
T_Session = Annotated[Session, Depends(get_session)]
T_current_user = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserResponse)
def create_user(user: UserRequest, session: T_Session):
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


@router.get('/', response_model=list[UserResponse])
def read_users(
    session: T_Session,
    current_user: T_current_user,
    limit: int = 10,
    offset: int = 0,
):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return users


@router.get('/{id:int}', response_model=UserResponse)
def read_user_by_id(
    id: int,
    current_user: T_current_user,
):
    if current_user.id != id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission'
        )
    return current_user


@router.put('/{id:int}', status_code=HTTPStatus.NO_CONTENT)
def update_user(
    id: int,
    user: UserRequest,
    session: T_Session,
    current_user: T_current_user,
):
    if current_user.id != id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission'
        )
    current_user.username = user.username
    current_user.password = get_password_hash(user.password)
    current_user.name = user.name
    current_user.email = user.email
    current_user.phone = user.phone
    session.commit()


@router.delete('/{id:int}', status_code=HTTPStatus.NO_CONTENT)
def delete_user(
    id: int,
    session: T_Session,
    current_user: T_current_user,
):
    if current_user.id != id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission'
        )
    session.delete(current_user)
    session.commit()
