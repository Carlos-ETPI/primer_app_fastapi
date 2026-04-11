
from datetime import timedelta
from typing import Annotated, Any
from fastapi import Response, APIRouter, Depends, HTTPException
from fastapi import security
from fastapi.security import OAuth2PasswordRequestForm

from app.database import SessionDep
from app.core.config import settings
from app.models.users import Token
import crud
from app.core import security
router = APIRouter(tags=["Login"])

@router.post("/login/access-token")
def login_access_token(
    response: Response,
    session: SessionDep, 
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = Token(
        access_token=security.create_access_token(
        user.id, expires_delta=access_token_expires
        ))
    
    response.set_cookie(
        key="access_token", 
        value=token.access_token, 
        httponly=True, 
        secure=True,    
        samesite="strict", 
        max_age=3600   
    )
    return {'message': 'login Exitoso'}
    #return token

# @router.post("/login/access-token")
# def login_access_token(
#     session: SessionDep, 
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
# ) -> Token:
#     # SI VIENEN DATOS DE USUARIO
#     if form_data.username and form_data.password:
#         user = crud.user.authenticate(session, email=form_data.username, password=form_data.password)
#         if user:
#             return Token(access_token=security.create_access_token(user.id, ...))

#     # SI VIENEN DATOS DE CLIENTE (MÁQUINA)
#     if form_data.client_id and form_data.client_secret:
#         client = crud.client.authenticate(session, client_id=form_data.client_id, client_secret=form_data.client_secret)
#         if client:
#             # Aquí el 'sub' del token sería el client_id
#             return Token(access_token=security.create_access_token(client.client_id, ...))
    
#     raise HTTPException(status_code=400, detail="Credenciales insuficientes")

@router.post("/login/access-token-plano")
def login_access_token(
    response: Response,
    session: SessionDep, 
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = Token(
        access_token=security.create_access_token(
        user.id, expires_delta=access_token_expires
        ))
    
    return token