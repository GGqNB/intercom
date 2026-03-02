
from sqlalchemy.ext.asyncio import AsyncSession
from src.crm.build.models import Entry, House
from src.crm.build.schemas import ReadHouse, WriteHouse, ReadEntry, \
    WriteEntry, FilterHouse, FilterEntry
from sqlalchemy import delete, func, insert, select, update
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import selectinload
from fastapi import Depends, HTTPException
from fastapi import APIRouter, status

async def get_house(
                    filters_params: FilterHouse,
                    session: AsyncSession):
    try:
        query = select(House).options(selectinload(House.city)) 
        if filters_params.geo_adress:
             query = query.filter(House.geo_adress.ilike(f'%{filters_params.geo_adress}%'))

        return await paginate(session, query)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "args": str(e),  
            }
        )

async def new_house(
                    new_event: WriteHouse,
                    session: AsyncSession):
    try:
        stmt = insert(House).values(new_event.model_dump()).returning(House) 
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

async def del_house(
                    house_id: int,
                    session: AsyncSession):
    try: 
        query = delete(House).where( 
            House.id == house_id 
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
    
async def change_house(
                    house_id: int,
                    updated_block: WriteHouse, 
                    session: AsyncSession):
    try:
        query = select(House).where(House.id == house_id)
        result = await session.execute(query)
        existing_block = result.scalar_one_or_none()  

        if existing_block is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Block with id {house_id} not found",
            )

        stmt = (
            update(House)
            .where(House.id == house_id)
            .values(updated_block.model_dump())
            .returning(House)
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

async def get_entry(
                    filters_params: FilterEntry,
                    session: AsyncSession):
    try:
        if filters_params.geo_adress:
            query = query.filter(Entry.house.geo_adress.ilike(f'%{filters_params.geo_adress}%'))
        elif filters_params.name:
            query = query.filter(Entry.name.ilike(f'%{filters_params.name}%'))
        else:
            query = select(Entry).options(selectinload(Entry.house)) 

        return await paginate(session, query)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "args": str(e),  
            }
        )