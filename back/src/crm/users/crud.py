from sqlalchemy.ext.asyncio import AsyncSession
from src.crm.stown.models import SFlat
from src.crm.intercom.schemas import  FilterIntecom
from sqlalchemy import delete, func, insert, select, update
from fastapi import Depends, HTTPException
from fastapi import APIRouter, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import selectinload
from src.crm.intercom.models import Intercom
from src.crm.users.models import Users
async def get_intercom(
                    filters_params: FilterIntecom,
                    session: AsyncSession):
    try:
        query = select(Intercom).options(selectinload(Intercom.entry)) 
        if filters_params.name:
             query = query.filter(Intercom.name.ilike(f'%{filters_params.name}%'))
        if filters_params.entry_id:
            query = query.filter(Intercom.entry_id == filters_params.entry_id)
        return await paginate(session, query)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "args": str(e),  
            }
        )
    
async def get_user_by_max_id_service(
    session: AsyncSession,
    max_id: str
) -> Users | None:


    query = (
        select(Users)
        .options(selectinload(Users.house))
        .where(Users.max_id == max_id)
    )

    result = await session.execute(query)
    return result.scalars().all()