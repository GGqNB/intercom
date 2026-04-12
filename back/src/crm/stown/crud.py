from sqlalchemy.ext.asyncio import AsyncSession
from src.crm.stown.models import SFlat
from src.crm.stown.schemas import ReadSFlat
from sqlalchemy import delete, func, insert, select, update
from fastapi import Depends, HTTPException
from fastapi import APIRouter, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import selectinload

        
async def upsert_flat(session: AsyncSession, data: ReadSFlat, house_id: int):
    stmt = select(SFlat).where(SFlat.id == data.id)
    result = await session.execute(stmt)
    flat = result.scalar_one_or_none()

    if flat:
        flat.type = data.type
        flat.number = data.number
        flat.ext_number = data.ext_number
        flat.house_id = house_id
    else:
        flat = SFlat(
            id=data.id,
            type=data.type,
            number=data.number,
            ext_number=data.ext_number,
            house_id=house_id
        )
        session.add(flat)

    await session.commit()
    await session.refresh(flat)
    return flat

async def get_flat_by_house(session: AsyncSession, house_id: int, number: int) -> int | None:

    try:
        stmt = select(SFlat.id).where(
        SFlat.house_id == house_id,
        SFlat.number == number,
        SFlat.type == 'Квартира'
    )
        result = await session.execute(stmt)
        flat_id = result.scalars().first()
        return flat_id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
        
