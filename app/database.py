from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine
from environs import Env

from app.core.config import settings


"""cuidado com los caracteres especiales en las contraseñas debe usar   
    from urllib.parse import quote_plus
    password_segura = quote_plus(env('DB_PASSWORD'))"""

postgres_url = settings.DATABASE_URL

"""echo solo debe usarse en desarrollo para ver las consultas SQL 
generadas como debug"""
#engine = create_engine(postgres_url,echo=True)
engine = create_engine(
    postgres_url,
    pool_pre_ping=True,
    pool_size=10, 
    max_overflow=20)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]