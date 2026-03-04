from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import selectinload
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi.security.api_key import APIKey

from src.crm.stown.crud import get_flat_by_house
from src.crm.users.methods import validate_flat
from src.crm.users.models import Users
from src.crm.users.schemas import ReadUser, WriteUser, FilterUser
from src.database import get_async_session
from src.auth import get_api_key, get_bot_key
from src.crm.build.models import House  # для join

router_users = APIRouter(prefix="/users", tags=["Users"])

@router_users.get("/list", response_model=Page[ReadUser])
async def get_users(
    filters_params: FilterUser = Depends(),
    session: AsyncSession = Depends(get_async_session),
    bot_key: APIKey = Depends(get_bot_key)
):
    try:
        query = select(Users).options(selectinload(Users.house)) 
        
        if filters_params.name:
            query = query.where(Users.name.ilike(f"%{filters_params.name}%"))
        if filters_params.chat_id:
            query = query.where(Users.chat_id.ilike(f"%{filters_params.chat_id}%"))
        if filters_params.max_id:
            query = query.where(Users.max_id.ilike(f"%{filters_params.max_id}%"))
        if filters_params.flat:
            query = query.where(Users.flat == filters_params.flat)
        if filters_params.flat_stown:
            query = query.where(Users.flat == filters_params.flat_stown)
        if filters_params.house_id:
            query = query.join(House, Users.house_id == House.id).where(Users.house_id == filters_params.house_id)

        return await paginate(session, query)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": status.HTTP_500_INTERNAL_SERVER_ERROR, "args": str(e)}
        )


@router_users.post("", status_code=status.HTTP_201_CREATED)
async def add_user(
    new_user: WriteUser,
    session: AsyncSession = Depends(get_async_session),
    bot_key: APIKey = Depends(get_bot_key)
):
    try:
        await validate_flat(session, new_user.house_id, new_user.flat)
        flat_id_stown = await get_flat_by_house(session, new_user.house_id, new_user.flat)
        new_user.flat_stown = flat_id_stown
        stmt = insert(Users).values(new_user.model_dump()).returning(Users)
        result = await session.execute(stmt)
        await session.commit()
        created_user = result.scalar_one()
        return {"data": created_user, "status": "success"}

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": str(e), "args": getattr(e, "args", None)}
        )


@router_users.patch("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
    user_id: int,
    flat: int | None = None,
    house_id: int | None = None,
    session: AsyncSession = Depends(get_async_session),
    api_key: APIKey = Depends(get_api_key)
):
    try:
        await validate_flat(session, house_id, flat)
        update_data = {}
        if flat is not None:
            update_data["flat"] = flat
        if house_id is not None:
            update_data["house_id"] = house_id
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update provided")
        
        stmt = update(Users).where(Users.id == user_id).values(**update_data).returning(Users)
        result = await session.execute(stmt)
        await session.commit()
        updated_user = result.scalar_one_or_none()
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"data": updated_user, "status": "success"}

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": str(e), "args": getattr(e, "args", None)}
        )


@router_users.patch("/by-max-id/{max_id}", status_code=status.HTTP_200_OK)
async def update_user_by_max_id(
    max_id: str,
    flat: int | None = None,
    house_id: int | None = None,
    session: AsyncSession = Depends(get_async_session),
    api_key: APIKey = Depends(get_api_key)
):
    try:
        await validate_flat(session, house_id, flat)
        
        update_data = {}
        if flat is not None:
            update_data["flat"] = flat
        if house_id is not None:
            update_data["house_id"] = house_id
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update provided")
        
        stmt = update(Users).where(Users.max_id == max_id).values(**update_data).returning(Users)
        result = await session.execute(stmt)
        await session.commit()
        updated_user = result.scalar_one_or_none()
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found with given max_id")
        return {"data": updated_user, "status": "success"}

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": str(e), "args": getattr(e, "args", None)}
        )


# -----------------------------
# DELETE: Удаление пользователя по ID
# -----------------------------
@router_users.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    api_key: APIKey = Depends(get_api_key)
):
    try:
        stmt = delete(Users).where(Users.id == user_id).returning(Users)
        result = await session.execute(stmt)
        await session.commit()
        deleted_user = result.scalar_one_or_none()
        if not deleted_user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"data": deleted_user, "status": "deleted"}

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": str(e), "args": getattr(e, "args", None)}
        )


# -----------------------------
# DELETE: Удаление пользователя по max_id
# -----------------------------
@router_users.delete("/by-max-id/{max_id}", status_code=status.HTTP_200_OK)
async def delete_user_by_max_id(
    max_id: str,
    session: AsyncSession = Depends(get_async_session),
    api_key: APIKey = Depends(get_api_key)
):
    try:
        stmt = delete(Users).where(Users.max_id == max_id).returning(Users)
        result = await session.execute(stmt)
        await session.commit()
        deleted_user = result.scalar_one_or_none()
        if not deleted_user:
            raise HTTPException(status_code=404, detail="User not found with given max_id")
        return {"data": deleted_user, "status": "deleted"}

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": str(e), "args": getattr(e, "args", None)}
        )