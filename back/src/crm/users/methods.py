from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.crm.build.models import House
from src.crm.users.models import Users

async def validate_flat(session: AsyncSession, house_id: int, flat: int):
    try:
        stmt = select(House).where(House.id == house_id)
        result = await session.execute(stmt)
        house = result.scalar_one_or_none()
        if not house:
            raise HTTPException(status_code=404, detail="House not found")

        if flat < 1 or flat > house.flat_count:
            raise HTTPException(
                status_code=400,
                detail=f"Квартира не находится в диапозоне"
            )
    except:
        raise HTTPException(
                status_code=400,
                detail=f"Ошибка, либо нет дома, либо квартира не в диапозоне"
            )

async def get_users_by_house_and_flat(
    session: AsyncSession,
    house_id: int,
    flat: int
) -> list[Users]:

    query = select(Users).where(
        Users.house_id == house_id,
        Users.flat == flat
    )

    result = await session.execute(query)
    return result.scalars().all()