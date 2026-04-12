import requests
from sqlalchemy.ext.asyncio import AsyncSession
from src.crm.stown.models import SFlat
from src.config import get_config
from src.crm.helper.stown import get_access_token
from src.redis_client import redis_client
from sqlalchemy import delete, func, insert, select, update
from fastapi import Depends, HTTPException
from fastapi import APIRouter, status
from fastapi_pagination.ext.sqlalchemy import paginate

conf = get_config()

async def flat_by_phone(phone):
    try:
        token = redis_client.get(conf.redis.STOWN_KEY)
        if not token:
            token = get_access_token()
            redis_client.set(conf.redis.STOWN_KEY, token)

        headers = {'Authorization': f'JWT {token}'}
        url = conf.stown.FLAT_BY_NUBMER_URL.format(phone=phone)
        print(url)
        
        api_response = requests.post(url, headers=headers)
        print(api_response.json())
        
        if api_response.status_code == 401:
            print("Token expired, getting new token...")
            token = get_access_token()
            redis_client.set(conf.redis.STOWN_KEY, token)
            
            headers = {'Authorization': f'JWT {token}'}
            api_response = requests.post(url, headers=headers)
            print(api_response.json())
        
        if api_response.status_code != 200:
            raise Exception("Stown API error: " + api_response.text)

        data = api_response.json()

        return {
            "status": data,
        }

    except Exception as e:
        return {"error": str(e)}
    

async def get_flat_number_by_ids(
    session: AsyncSession,
    house_id: int,
    flat_id: int
) -> int | None:

    stmt = select(SFlat.number).where(
        SFlat.id == flat_id,
        SFlat.house_id == house_id
    )

    result = await session.execute(stmt)
    return result.scalar()
    # print(house_id, flat_id)
    # stmt = select(SFlat.number).where(
    # SFlat.id == flat_id
    # )

    # result = await session.execute(stmt)
    # flat_number = result.scalar()

    # return flat_number
    # print('Ыу   ')
    # try:
    #     stmt = select(SFlat).where(
    #     # SFlat.house_id == house_id,
    #     SFlat.id == flat_id,
    #     # SFlat.type == 'Квартира'
    # )
    #     result = await session.execute(stmt)
    #     flat_id = result.scalars().first()
    #     return flat_id
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=str(e)
    #     )