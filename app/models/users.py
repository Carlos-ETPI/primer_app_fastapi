from sqlmodel import Field, Relationship, SQLModel

from app.models.audit import AuditMixin
from app.models.rol import Rol
from app.models.user_rol import UserRol


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True  )
    email : str = Field(index=True, unique=True)
    nombre : str = Field(index=True)
    apellido : str = Field(index=True)
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    password : str = Field(min_length=6)


class UserRead(UserBase):
    id : int


class UserUpdate(UserBase):
    pass

class User(UserBase,AuditMixin, table=True):
    id : int = Field(default=None, primary_key=True)
    password : str = Field(min_length=6)

    rols : list["Rol"] =Relationship(back_populates="users", link_model=UserRol)

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None