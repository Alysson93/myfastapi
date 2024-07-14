from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import get_session
from models import User
from schemas import Token
from security import create_access_token, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])
T_Session = Annotated[Session, Depends(get_session)]


@router.post('/token', response_model=Token)
def token(
    session: T_Session, form_data: OAuth2PasswordRequestForm = Depends()
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
