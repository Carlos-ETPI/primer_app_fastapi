from fastapi import APIRouter, HTTPException,status
from sqlmodel import select

from app.core.security import get_password_hash
from app.database import SessionDep
from app.dependencies import CurrentUser
from app.models.users import UserCreate, UserRead, User

router = APIRouter(tags=["Users"])
@router.post("/users",response_model=UserRead)
async def create_user(user_data : UserCreate, session : SessionDep):
    user_dict = user_data.model_dump()
    plain_password = user_dict.pop("password")
    hashed_password = get_password_hash(plain_password)
    
    # 3. Creamos el objeto User manualmente con la contraseña encriptada
    user_db = User(**user_dict, password=hashed_password)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db


@router.get("/users", response_model=list[UserRead])
async def get_users(session : SessionDep, current_user: CurrentUser):
    statement = select(User)
    resultados = session.exec(statement).all()
    return resultados