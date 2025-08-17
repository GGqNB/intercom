
from fastapi import APIRouter, status
from src.crm.build.crud import get_house, new_house, \
    del_house, change_house, get_entry
from src.database import get_async_session
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from src.crm.build.models import House
from src.crm.build.models import Entry
from src.crm.build.schemas import ReadHouse, WriteHouse, \
      ReadEntry, WriteEntry, FilterHouse, FilterEntry
from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.orm import selectinload
from fastapi.security.api_key import APIKey
from src.auth import get_api_key

router_build = APIRouter(
    prefix="/build",
    tags=["Работа с домом и входами"]
)


@router_build.get("/house", response_model=Page[ReadHouse])
async def read_house(
    filters_params: FilterHouse = Depends(),
    session: AsyncSession = Depends(get_async_session),
    api_key: APIKey = Depends(get_api_key)
):
    return await get_house(filters_params = filters_params, session = session)

@router_build.post("/house",  status_code=status.HTTP_201_CREATED)
async def create_house(
    new_event: WriteHouse,
    session: AsyncSession = Depends(get_async_session),
    api_key: APIKey = Depends(get_api_key)

):
   return await new_house(new_event = new_event, session = session)
    
@router_build.delete("/house/{house_id}") 
async def delete_house( 
        house_id: int, 
        session: AsyncSession = Depends(get_async_session), 
        api_key: APIKey = Depends(get_api_key)

): 
     return await del_house(house_id = house_id, session = session)

@router_build.put("/house/{house_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_house(
    house_id: int,
    updated_house: WriteHouse, 
    session: AsyncSession = Depends(get_async_session),
    api_key: APIKey = Depends(get_api_key)

):
    return await change_house(house_id = house_id, updated_house = updated_house, session = session)

@router_build.get("/entry", response_model=Page[ReadEntry])
async def read_entry(
    filters_params: FilterEntry = Depends(),
    session: AsyncSession = Depends(get_async_session),
    api_key: APIKey = Depends(get_api_key)
):
    try:
        query = select(Entry).options(selectinload(Entry.house))  # Инициализируйте query здесь

        if filters_params.geo_adress:
            query = query.join(House, Entry.house_id == House.id)  # Явное указание join-а
            query = query.where(House.geo_adress.ilike(f"%{filters_params.geo_adress}%"))
            # query = query.where(Entry.house.has(geo_adress=filters_params.geo_adress))  # Corrected Geo Adress to use where
        if filters_params.name:
            query = query.where(Entry.name.ilike(f"%{filters_params.name}%")) # Corrected Entry Name
        if filters_params.house_id:
            query = query.filter(Entry.house_id == filters_params.house_id)
        return await paginate(session, query)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "args": str(e),
            }
        )


@router_build.post("/entry",  status_code=status.HTTP_201_CREATED, description="Создание входа(Калитка, подъезд  и др.)")
async def add_entry(
    new_event: WriteEntry,
    session: AsyncSession = Depends(get_async_session),
    api_key: APIKey = Depends(get_api_key)

):
    try:
        stmt = insert(Entry).values(new_event.model_dump()).returning(Entry) 
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
    
@router_build.delete("/entry/{id}") 
async def delete_entry( 
        id: int, 
        session: AsyncSession = Depends(get_async_session), 
        api_key: APIKey = Depends(get_api_key)

): 
    try: 
        query = delete(Entry).where( 
            Entry.id == id 
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

@router_build.put("/entry/{house_id}",status_code=status.HTTP_202_ACCEPTED)
async def update_entry(
    house_id: int,
    updated_block: WriteEntry, 
    session: AsyncSession = Depends(get_async_session),
    api_key: APIKey = Depends(get_api_key)

):
    try:
        query = select(Entry).where(Entry.id == house_id)
        result = await session.execute(query)
        existing_block = result.scalar_one_or_none()  

        if existing_block is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Block with id {house_id} not found",
            )

        stmt = (
            update(Entry)
            .where(Entry.id == house_id)
            .values(updated_block.model_dump())
            .returning(Entry)
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
    
