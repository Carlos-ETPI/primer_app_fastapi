from typing import List
from fastapi import APIRouter, HTTPException,status
from sqlmodel import select

from app.models.models import InventoryMovement, InventoryMovementCreate, InventoryMovementRead, Product, TransactionType
from app.database import SessionDep

router = APIRouter(tags=["Movements"])


@router.post("/movements", response_model=InventoryMovementRead)
async def create_movement(movement_data : InventoryMovementCreate, session : SessionDep):
    movement_db = InventoryMovement.model_validate(movement_data.model_dump())
    product = session.get(Product, movement_data.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no existe"
        )
    if movement_data.transaction == "SALIDA":
        if product.stock < movement_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Stock insuficiente para la salida"
            )
        product.stock -= movement_data.quantity

    elif movement_data.transaction == "ENTRADA":
        product.stock += movement_data.quantity

    elif movement_data.transaction == "AJUSTE":
        diferencia_real = movement_data.quantity - product.stock
        product.stock = movement_data.quantity
        movement_db.quantity = diferencia_real

    else :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de transaccion no valido."
        )
    session.add(movement_db)
    session.add(product)
    session.commit()
    session.refresh(movement_db)
    return movement_db


@router.get("/movements", response_model=list[InventoryMovementRead])
async def get_movements(session : SessionDep):
    statement = select(InventoryMovement)
    resultados = session.exec(statement).all()
    return resultados


@router.get("/movements/types", response_model=List[str])
def get_transaction_types():
    return [t.value for t in TransactionType]