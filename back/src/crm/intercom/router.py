
from fastapi import APIRouter, status
from src.database import get_async_session
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from src.crm.intercom.models import Intercom
from src.crm.intercom.schemas import ReadIntercom, WrhiteIntercom, FilterIntecom
from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.orm import selectinload
from src.crm.intercom.crud import get_intercom
from fastapi.security.api_key import APIKey
from src.auth import get_api_key

router_intercom = APIRouter(
    prefix="/intercom",
    tags=["Работа с домофоном"]
)


@router_intercom.get("", response_model=Page[ReadIntercom])
async def read_intercom(
    filters_params: FilterIntecom = Depends(),
    session: AsyncSession = Depends(get_async_session),
    api_key: APIKey = Depends(get_api_key)

):
     return await get_intercom(filters_params = filters_params, session = session)

@router_intercom.post("",  status_code=status.HTTP_201_CREATED)
async def add_intercom(
    new_event: WrhiteIntercom,
    session: AsyncSession = Depends(get_async_session),
    api_key: APIKey = Depends(get_api_key)

):
    try:
        stmt = insert(Intercom).values(new_event.model_dump()).returning(Intercom) 
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
    
@router_intercom.delete("/{id}") 
async def delete_intercom( 
        id: int, 
        session: AsyncSession = Depends(get_async_session), 
        api_key: APIKey = Depends(get_api_key)

): 
    try: 
        query = delete(Intercom).where( 
            Intercom.id == id 
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

@router_intercom.put("/{block_id}",status_code=status.HTTP_202_ACCEPTED)
async def update_intercom(
    block_id: int,
    updated_block: WrhiteIntercom, 
    session: AsyncSession = Depends(get_async_session),
    api_key: APIKey = Depends(get_api_key)

):
    try:
        query = select(Intercom).where(Intercom.id == block_id)
        result = await session.execute(query)
        existing_block = result.scalar_one_or_none()  

        if existing_block is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Block with id {block_id} not found",
            )

        stmt = (
            update(Intercom)
            .where(Intercom.id == block_id)
            .values(updated_block.model_dump())
            .returning(Intercom)
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
