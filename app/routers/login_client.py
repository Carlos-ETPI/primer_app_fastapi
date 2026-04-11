from datetime import timedelta
from multiprocessing.connection import Client
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app import routers
from app.core import security
from app.core.config import Settings
from app.database import SessionDep

router = APIRouter(tags=["Login Client"])

@router.post("/login/client-token")
def login_client_credentials(
    session: SessionDep,
    client_id: str,
    client_secret: str
):
    # 1. Buscar cliente
    statement = select(Client).where(Client.client_id == client_id)
    client = session.exec(statement).first()
    
    # 2. Verificar secreto (puedes reusar tu verify_password)
    verified, _ = security.verify_password(client_secret, client.client_secret_hash)
    if not verified:
        raise HTTPException(status_code=400, detail="Credenciales de cliente incorrectas")
    
    # 3. Crear token
    access_token_expires = timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            client.client_id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }