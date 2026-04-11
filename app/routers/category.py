from datetime import date

from fastapi import APIRouter, Depends, HTTPException,status
from sqlmodel import select

from app.dependencies import CurrentUser, CurrentUser2
from app.models.models import Category,CategoryCreate,CategoryRead, CategoryReportRead, CategoryUpdate
from app.database import SessionDep
#from app.dependencies import SecurityChecker


router = APIRouter(tags=["Categories"])


@router.post("/categorys", response_model=CategoryRead)
async def create_category(
    category_data: CategoryCreate,
    session: SessionDep,
    current_user: CurrentUser): #= Depends(SecurityChecker(allowed_roles=["admin", "empleado"])
    #current_user: CurrentUser(allowed_roles=["admin"])

    """aqui se convierte el objeto pydantic a un diccionario, se excluyen los campos que no se han enviado en la peticion, en este caso no se envia el campo created_by, por lo que se excluye del diccionario"""
    category_dict = category_data.model_dump(exclude_unset=True)
    """aqui se agrega el campo created_by al diccionario, con el valor del username del usuario que ha creado la categoria"""
    category_dict["created_by"] = current_user.username
    """aqui se comvirte el objeto pydantic a un objeto sqlmodel, se puede hacer de dos formas, una es usando el metodo model_validate y la otra es usando el constructor de la clase"""
    category_db = Category.model_validate(category_dict)
    #category_db = Category(**category_dict)
    session.add(category_db)
    session.commit()
    session.refresh(category_db)
    return category_db


@router.get("/categorys", response_model=list[CategoryRead])
async def get_categorys(
    session: SessionDep,
    current_user2: CurrentUser2,
    name : str = None,
    page : int = 1,
    size : int = 5): #= Depends(
        #SecurityChecker(allowed_roles=["admin", "empleado"]))
    offset = (page - 1) * size
    category_db = select(Category)
    print(category_db)
    if name:
        category_db = category_db.where(Category.name.ilike(f"%{name}%"))

    return session.exec(category_db.offset(offset).limit(size)).all()


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


@router.get("/categorys/{name}",response_model=list[CategoryRead])
def search_category(
    name : str,
    session : SessionDep, 
    current_user : CurrentUser ):#= Depends(SecurityChecker(allowed_roles=["admin", "empleado"]))):
    category_db = session.exec(select(Category).where(Category.name.ilike(f"%{name}%"))).all()
    if not category_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria no existe"
        )
    return category_db


@router.post("/categorys/report/date", response_model=list[CategoryRead])
def report_category(
    session : SessionDep, 
    current_user : CurrentUser, 
    category_report : CategoryReportRead):

    report_db = session.exec(select(Category).where((Category.created_at >= category_report.fecha_inicio) & (Category.created_at <= category_report.fecha_fin))).all()
    if not report_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron categorias en el rango de fechas especificado"
        )    
    return report_db


@router.get("/category/report/date/{fecha_inicio}/{fecha_fin}", response_model=list[CategoryRead])
def report_category_by_date(
    session : SessionDep, 
    current_user : CurrentUser, 
    fecha_inicio: date,
    fecha_fin: date):
    report_db = session.exec(select(Category).where((Category.created_at >= fecha_inicio) & (Category.created_at <= fecha_fin))).all()
    if not report_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron categorias en el rango de fechas especificado"
        )    
    return report_db