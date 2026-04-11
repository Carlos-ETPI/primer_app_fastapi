from multiprocessing.connection import Client
from typing import Annotated
from environs import ValidationError
from fastapi import Depends, HTTPException, Request, Security, status
from fastapi.security import APIKeyHeader, OAuth2, OAuth2PasswordBearer
import jwt
from sqlmodel import select

from app.database import SessionDep
from app.models.users import TokenPayload, User
from app.core.config import settings
from app.core import security

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

TokenDep = Annotated[str, Depends(reusable_oauth2)]

def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Credenciales no válidas",
        )
    user = session.get(User, token_data.sub)

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return user.model_dump(exclude={"password"})

CurrentUser = Annotated[User, Depends(get_current_user)]
# def CurrentUser(allowed_roles: list[str] = None, required_permission: str = None):
#     return Annotated[User, Depends(SecurityChecker(allowed_roles, required_permission))]


def get_current_client(session: SessionDep, token: TokenDep) -> Client:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token de cliente no válido",
        )
    
    # Buscamos en la tabla de Client
    statement = select(Client).where(Client.client_id == token_data.sub)
    client = session.exec(statement).first()
    
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no registrado")
    if not client.is_active:
        raise HTTPException(status_code=400, detail="Cliente inactivo")
    return client

CurrentClient = Annotated[Client, Depends(get_current_client)]




# def get_current_active_superuser(current_user: CurrentUser) -> User:
#     if not current_user.is_superuser:
#         raise HTTPException(
#             status_code=403, detail="El usuario no tiene privilegios suficientes"
#         )
#     return current_user


# class SecurityChecker:
#     def __init__(self, allowed_roles: list[str] = None, required_permission: str = None):
#         self.allowed_roles = allowed_roles or []
#         self.required_permission = required_permission

#     def __call__(self, user: User = Depends(get_current_user)):
#         # 1. El Superusuario siempre pasa (Tu llave maestra)
#         if user.is_superuser:
#             return user

#         # 2. Verificar por ROL
#         # Extraemos los nombres de los roles del usuario desde la tabla 'userrol'
#         user_role_names = [ur.rol.name for ur in user.user_roles]
#         for role in self.allowed_roles:
#             if role in user_role_names:
#                 return user

#         # 3. Verificar por PERMISO (Si no pasó por rol)
#         if self.required_permission:
#             # Buscamos en todos los roles del usuario si alguno tiene el permiso
#             for ur in user.user_roles:
#                 permission_names = [rp.permission.name for rp in ur.rol.rol_permissions]
#                 if self.required_permission in permission_names:
#                     return user

#         # 4. Si llegó aquí, no tiene acceso
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="No tienes el rol o permiso necesario"
#         )
# class SecurityChecker:
#     def __init__(self, allowed_roles: list[str] = None, required_permission: str = None):
#         self.allowed_roles = allowed_roles or []
#         self.required_permission = required_permission

#     def __call__(self, user: User = Depends(get_current_user)):
#         """esta parte solo se activa si los superusarios no necesitan pasar por los chequeos de rol/permiso"""
#         # if user.is_superuser:
#         #     return user

#         user_roles = [rol.name for rol in user.rols] 
#         if any(role in user_roles for role in self.allowed_roles):
#             return user

#         if self.required_permission:
#             for ur in user.user_roles:
#                 permissions = [rp.permission.name for rp in ur.rol.rol_permissions]
#                 if self.required_permission in permissions:
#                     return user

#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, 
#             detail="No tienes los privilegios necesarios"
#         )
    
def audit_create(current_user: CurrentUser):
    return {
        "created_by": current_user.username
    }


"""Ejemplo de API Key para clientes externos (no usuarios humanos)"""

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == settings.API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="API Key inválida")

ApiKey = Annotated[str, Depends(get_api_key)]






class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(self, tokenUrl: str, auto_error: bool = True):
        flows = {
            "password": {
                "tokenUrl": tokenUrl,
                "scopes": {}
            }
        }
        super().__init__(flows=flows, auto_error=auto_error)

    async def __call__(self, request: Request):
        cookie_token = request.cookies.get("access_token")
        if cookie_token:
            return cookie_token

        if self.auto_error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No autenticado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return None
oauth2_scheme_cookie = OAuth2PasswordBearerWithCookie(tokenUrl=f"{settings.API_V1_STR}/login/access-token")

TokenCookie = Annotated[str, Depends(oauth2_scheme_cookie)]

def get_current_user2(token_cookie: TokenCookie, session: SessionDep ) -> User:
    token = token_cookie
    if not token:
        raise HTTPException(
            status_code=401, 
            detail="No hay token de acceso")
    try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
            )
            token_data = TokenPayload(**payload)
    except (jwt.InvalidTokenError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token de cliente no válido",
            )
    
    user = session.get(User, token_data.sub)

    if not user:
        raise HTTPException(status_code=404,
                            detail="Usuario no encontrado")
    if not user.is_active:
        raise HTTPException(status_code=400, 
                            detail="Usuario inactivo")
    return user.model_dump(exclude={"password"})

CurrentUser2 = Annotated[User, Depends(get_current_user2)]