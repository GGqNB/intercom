
from fastapi import APIRouter, status
from src.crm.helper.faker import generate_fake_list
from src.database import get_async_session
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from src.crm.location.models import City
from src.crm.location.schemas import ReadCity, BaseCity
from sqlalchemy import delete, func, insert, select, update

router_location = APIRouter(
    prefix="/city",
    tags=["Работа с локацией"]
)


@router_location.get("/fake_cities/")
async def get_fake_cities(count: int = 10):
    """
    Генерирует список фейковых городов.  (Возвращает Pydantic модели)
    """
    return generate_fake_list(ReadCity, count)

@router_location.get("", response_model=Page[ReadCity])
async def get_user(
    session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(City)
        
        count_query = select(func.count()).select_from(City)

        return await paginate(session, query)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "args": str(e),  
            }
        )

@router_location.post("",  status_code=status.HTTP_201_CREATED)
async def add_event(
    new_event: BaseCity,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        stmt = insert(City).values(new_event.model_dump()).returning(City) 
        result = await session.execute(stmt)
        await session.commit()
        created_event = result.scalar_one()  #

        return {
            "data" : created_event,
            "status" : "success"
        }
    except Exception as e:
        await session.rollback() 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e), 
                "args": e.args if hasattr(e, 'args') else None,
            }
        )
    
@router_location.delete("/{id}") 
async def delete_event( 
        id: int, 
        session: AsyncSession = Depends(get_async_session), 
): 
    try: 
        query = delete(City).where( 
            City.id == id 
        ) 
        await session.execute(query) 
        await session.commit() 
        return { 
            "status": "success", 
            "details": "Удален" 
        } 
    except: 
        raise HTTPException( 
            status_code=500, 
            detail='Ошибка при удалении' 
        )

@router_location.put("/{block_id}",status_code=status.HTTP_202_ACCEPTED)
async def update_block(
    block_id: int,
    updated_block: BaseCity, 
    session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(City).where(City.id == block_id)
        result = await session.execute(query)
        existing_block = result.scalar_one_or_none()  

        if existing_block is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Block with id {block_id} not found",
            )

        stmt = (
            update(City)
            .where(City.id == block_id)
            .values(updated_block.model_dump())
            .returning(City)
        )
        result = await session.execute(stmt)
        await session.commit()
        updated_data = result.scalar_one()

        return {
            "data" : updated_data,
            "status" : "success"
        }  

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
                "args": e.args if hasattr(e, 'args') else None,
            }
        )