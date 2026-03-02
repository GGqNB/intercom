
from typing import Optional

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi import File, HTTPException, UploadFile, status

from src.crm.helper.image import compress_image_to_1mb, save_image
from src.crm.logs.models import CallLog
from src.crm.logs.schemas import WriteCallLog, FilterCallLog

async def get_call_logs(session: AsyncSession, filters: FilterCallLog):
    query = select(CallLog)

    if filters.type:
        query = query.where(CallLog.type == filters.type)

    if filters.house_id:
        query = query.where(CallLog.house_id == filters.house_id)

    if filters.flat:
        query = query.where(CallLog.flat == filters.flat)


    return await paginate(session, query)


async def create_call_log(session: AsyncSession, data: WriteCallLog):

    try:
        log = CallLog(**data.model_dump())

        session.add(log)
        await session.commit()
        await session.refresh(log)

        return log

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


async def update_call_log(session: AsyncSession, log_id: int, data: WriteCallLog):
    try:
        stmt = (
            update(CallLog)
            .where(CallLog.id == log_id)
            .values(data.model_dump())
            .returning(CallLog)
        )
        result = await session.execute(stmt)
        await session.commit()

        updated = result.scalar_one_or_none()
        if not updated:
            raise HTTPException(status_code=404, detail="Log not found")

        return updated

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail={"code": 500, "message": str(e)}
        )

async def update_call_log_photo(session: AsyncSession, log_id: int, photo: Optional[UploadFile] = File(None)):
    
    if not photo:
        raise HTTPException(status_code=400, detail="Фото не передано")

    try:
        # читаем файл
        file_bytes = await photo.read()

        # сжимаем
        compressed_bytes = compress_image_to_1mb(file_bytes)

        # сохраняем
        photo_path = save_image(compressed_bytes)

        # обновляем запись
        stmt = (
            update(CallLog)
            .where(CallLog.id == log_id)
            .values(photo_url=photo_path)
            .returning(CallLog)
        )

        result = await session.execute(stmt)
        await session.commit()

        updated_log = result.scalar_one_or_none()

        if not updated_log:
            raise HTTPException(status_code=404, detail="Log not found")

        return {
            "status": "photo updated",
            "data": updated_log
        }

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

async def delete_call_log(session: AsyncSession, log_id: int):
    try:
        stmt = delete(CallLog).where(CallLog.id == log_id)
        await session.execute(stmt)
        await session.commit()
        return {"status": "deleted"}

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail={"code": 500, "message": str(e)}
        )