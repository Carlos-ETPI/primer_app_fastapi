from fastapi import APIRouter, HTTPException,status
from sqlmodel import select

from app.dependencies import CurrentUser
from app.models.models import Category,CategoryCreate,CategoryRead, CategoryUpdate
from app.database import SessionDep

router = APIRouter(tags=["Categories"])

@router.post("/categorys", response_model=CategoryRead)
async def create_category(category_data : CategoryCreate, session : SessionDep,current_user: CurrentUser):
    category_db = Category.model_validate(category_data.model_dump())
    session.add(category_db)
    session.commit()
    session.refresh(category_db)
    return category_db


@router.get("/categorys", response_model=list[CategoryRead])
async def get_categorys(session : SessionDep, current_user: CurrentUser):
    statement = select(Category)
    resultados = session.exec(statement).all()
    return resultados


@router.delete("/categorys/{category_id}")
async def delete_category(category_id : int, session : SessionDep, current_user: CurrentUser):
    category_db = session.get(Category, category_id)
    if not category_db:
        raise HTTPException( 
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Categoria no existe")
    session.delete(category_db)
    session.commit()
    return {"detail":"Categoria eliminada con exito"}


@router.patch(
        "/categorys/{category_id}", 
        response_model=CategoryRead,
        status_code=status.HTTP_201_CREATED,
        )
async def update_category(
    category_id : int , 
    category_data : CategoryUpdate,
    session : SessionDep, 
    current_user: CurrentUser):

    category_db = session.get(Category, category_id)
    if not category_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Categoria no existe")
    category_data_dict = category_data.model_dump(exclude_unset=True)
    category_db.sqlmodel_update(category_data_dict)
    session.add(category_db)
    session.commit()
    session.refresh(category_db)
    return category_db