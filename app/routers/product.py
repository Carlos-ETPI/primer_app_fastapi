from fastapi import APIRouter, HTTPException,status
from sqlmodel import select

from app.database import SessionDep
from app.models.models import Product, ProductCreate, ProductRead

router = APIRouter(tags=["Products"])


@router.post("/products",response_model=ProductRead)
async def create_product(product_data : ProductCreate, session : SessionDep):
    product_db = Product.model_validate(product_data.model_dump())
    session.add(product_db)
    session.commit()
    session.refresh(product_db)
    return product_db


@router.get("/products",response_model=list[ProductRead])
async def get_products(session : SessionDep):
    return session.exec(select(Product)).all()


@router.delete("/products/{product_id}")
async def delete_product(product_id : int, session :SessionDep):
    product_db = session.get(Product, product_id)
    if not product_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no existe"
        )
    session.delete(product_db)
    session.commit()
    return {"detail":"Producto eliminado con exito."}


@router.post("/products/{product_id}", response_model=ProductRead)
async def search_product(product_id : int, session : SessionDep):
    product_db = session.get(Product,product_id)
    if not product_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no existe"
        )
    return product_db


