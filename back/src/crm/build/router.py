
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

router_build = APIRouter(
    prefix="/build",
    tags=["Работа с домом и входами"]
)


@router_build.get("/house", response_model=Page[ReadHouse])
async def read_house(
    filters_params: FilterHouse = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    return await get_house(filters_params = filters_params, session = session)

@router_build.post("/house",  status_code=status.HTTP_201_CREATED)
async def create_house(
    new_event: WriteHouse,
    session: AsyncSession = Depends(get_async_session),
):
   return await new_house(new_event = new_event, session = session)
    
@router_build.delete("/house/{house_id}") 
async def delete_house( 
        house_id: int, 
        session: AsyncSession = Depends(get_async_session), 
): 
     return await del_house(house_id = house_id, session = session)

@router_build.put("/house/{house_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_house(
    house_id: int,
    updated_house: WriteHouse, 
    session: AsyncSession = Depends(get_async_session),
):
    return await change_house(house_id = house_id, updated_house = updated_house, session = session)

@router_build.get("/entry", response_model=Page[ReadEntry])
async def read_entry(
    filters_params: FilterEntry = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(Entry).options(selectinload(Entry.house))  # Инициализируйте query здесь

        if filters_params.geo_adress:
            query = query.where(Entry.house.has(geo_adress=filters_params.geo_adress))  # Corrected Geo Adress to use where
        if filters_params.name:
            query = query.where(Entry.name.ilike(f"%{filters_params.name}%")) # Corrected Entry Name

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
    

# Андрей Дроган, [05.08.2025 14:35]
# async def get_ticket_worker(sort_params: TicketWorkerSortBy,
#                             filters_params: FilterTicketWorkerSchemas,
#                             page_params: PageParams,
#                             master_id: int,
#                             session: AsyncSession):
#     try:
#         IsActive = {"active": "active", "inactive": "inactive", "processing": "processing"}
#         query = select(TicketWorker).filter_by(master_id=master_id)
#         # Фильтры
#         if filters_params.fio:
#             query = query.filter(TicketWorker.fio.ilike(f'%{filters_params.fio}%'))
#         if filters_params.status:
#             query = query.filter_by(status=IsActive.get(filters_params.status.name))
#         if filters_params.email:
#             query = query.filter(TicketWorker.email.ilike(f'%{filters_params.email}%'))
#         if filters_params.stateorg_index:
#             query = query.filter_by(stateorg_index=filters_params.stateorg_index)
#         # Сортировка
#         order_column = getattr(TicketWorker, sort_params.sortBy.name)
#         if sort_params.descending:
#             order_column = desc(order_column)
#         query = query.order_by(order_column)
#         return await paginate(sort_params=sort_params, page_params=page_params, query=query,
#                               response_schema=ReadTicketWorkerSchemas, session=session)
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail={
#                 "code": 'dsa',
#                 "args": str(e),
#             }
#         )

# Андрей Дроган, [05.08.2025 14:35]
# class FilterTicketWorkerSchemas(BaseModel):
#     fio: Annotated[Optional[str], Field(default=None)]
#     email: Annotated[Optional[str], Field(default=None)]
#     stateorg_index: Annotated[Optional[int], Field(default=None)]
#     status: Annotated[Optional[IsActive], Field(default=None)]