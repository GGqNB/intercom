from src.crm.stown.models import SFlat
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import selectinload
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi.security.api_key import APIKey
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.crm.stown.methods import flat_by_phone
from src.crm.users.crud import get_user_by_max_id_service
from src.crm.stown.crud import get_flat_by_house
from src.crm.users.methods import validate_flat
from src.crm.users.models import Users
from src.crm.users.schemas import ReadUser, WriteUser, FilterUser, WriteUserMax
from src.database import get_async_session
from src.auth import get_api_key, get_bot_key
from src.crm.build.models import House  # для join

router_users = APIRouter(prefix="/users", tags=["Users"])

@router_users.get("/list", response_model=Page[ReadUser])
async def get_users(
    filters_params: FilterUser = Depends(),
    session: AsyncSession = Depends(get_async_session),
    api_key: APIKey = Depends(get_api_key)
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

@router_users.get("/{max_id}", response_model=list[ReadUser])
async def get_user_by_max_id(
    max_id: str,
    session: AsyncSession = Depends(get_async_session),
    bot_key: APIKey = Depends(get_bot_key)
):
    try:
        user = await get_user_by_max_id_service(session, max_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )

        return user

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e)
            }
        )

@router_users.post("", status_code=status.HTTP_201_CREATED)
async def add_user(
    new_user: WriteUser,
    session: AsyncSession = Depends(get_async_session),
    bot_key: APIKey = Depends(get_bot_key)
):
    try:
        await validate_flat(session, new_user.house_id, new_user.flat)

        flat_id_stown = await get_flat_by_house(
            session,
            new_user.house_id,
            new_user.flat
        )
        if not flat_id_stown:
            raise HTTPException(
                status_code=status.HTTP_418_IM_A_TEAPOT,
                detail="Квартира не найдена"
            )
        new_user.flat_stown = flat_id_stown

        stmt = insert(Users).values(new_user.model_dump())

        stmt = stmt.on_conflict_do_update(
            index_elements=["max_id"],  # поле с UNIQUE
            set_={
                "name": new_user.name,
                "chat_id": new_user.chat_id,
                "flat": new_user.flat,
                "flat_stown": new_user.flat_stown,
                "house_id": new_user.house_id
            }
        ).returning(Users)

        result = await session.execute(stmt)
        await session.commit()

        created_or_updated_user = result.scalar_one()

        return {
            "data": created_or_updated_user,
            "status": "success"
        }

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

from sqlalchemy import insert, delete, func
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException, status

@router_users.post("/max/{phone}", status_code=status.HTTP_201_CREATED)
async def add_user(
    phone: str,
    max_user: WriteUserMax,
    session: AsyncSession = Depends(get_async_session),
    bot_key: APIKey = Depends(get_bot_key)
):
    try:
        flats = await flat_by_phone(phone)
        
        flats_data = flats.get("status", [])
        if not flats_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Нет данных по номеру"
            )

        max_id_clean = max_user.max_id.strip() 
        delete_stmt = delete(Users).where(
            func.trim(Users.max_id) == max_id_clean
        ).returning(Users)
        deleted_result = await session.execute(delete_stmt)
        await session.commit() 

        users_to_insert = []
        seen = set()
      
        for build in flats_data:
            for home in build.get("homes", []):
                key = (
                    max_id_clean,
                    build["build_id"],
                    home["home_id"]
                )
                if key in seen:
                    continue
                seen.add(key)

                users_to_insert.append({
                    "name": max_user.name,
                    "chat_id": max_user.chat_id,
                    "max_id": max_id_clean,
                    "flat": int(home["home_number"]),
                    "house_id": build["build_id"],
                    "flat_stown": home["home_id"]
                })

        if not users_to_insert:
            return {
                "data": [],
                "count_deleted": len(deleted_result.scalars().all()),
                "count_created": 0,
                "status": "deleted_no_new_data"
            }

        insert_stmt = insert(Users).values(users_to_insert).returning(Users)
        result_insert = await session.execute(insert_stmt)
        await session.commit()

        created_users = result_insert.scalars().all()

        flat_stown_ids = [user.flat_stown for user in created_users if user.flat_stown]
        stown_flats = {}
        if flat_stown_ids:
            stown_flat_query = select(SFlat).where(SFlat.id.in_(flat_stown_ids))
            stown_flat_result = await session.execute(stown_flat_query)
            stown_flats = {sf.id: sf for sf in stown_flat_result.scalars().all()}

        response_data = []
        for user in created_users:
            user_dict = {
                "id": user.id,
                "max_id": user.max_id,
                "chat_id": user.chat_id,
                "name": user.name,
                "flat": user.flat,
                "house_id": user.house_id,
                "flat_stown": user.flat_stown,
                "stown_flat": None
            }

            if user.flat_stown and user.flat_stown in stown_flats:
                sf = stown_flats[user.flat_stown]
                user_dict["stown_flat"] = {
                    "id": sf.id,
                    "type": sf.type,
                    "number": sf.number,
                    "ext_number": sf.ext_number,
                    "house_id": sf.house_id
                }

            response_data.append(user_dict)

        return {
            "data": response_data,
            "count_deleted": len(deleted_result.scalars().all()),
            "count_created": len(created_users),
            "status": "success"
        }

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Такие данные уже существуют. Попробуйте восстановить доступ."
        )

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
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



@router_users.delete("/by-max-id/{max_id}", status_code=status.HTTP_200_OK)
async def delete_user_by_max_id(
    max_id: str,
    session: AsyncSession = Depends(get_async_session),
    api_key: APIKey = Depends(get_api_key)
):
    try:
        stmt = delete(Users).where(
            Users.max_id == max_id
        ).returning(Users)

        result = await session.execute(stmt)

        deleted_users = result.scalars().all() 

        if not deleted_users:
            await session.rollback()
            raise HTTPException(
                status_code=404,
                detail="Не нашлось таких пользователей"
            )

        await session.commit()

        return {
            "count": len(deleted_users),
            "status": "deleted"
        }

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )