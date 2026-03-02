
from fastapi import APIRouter, status
import requests
from sqlalchemy import func, select
from src.crm.stown.models import SFlat
from src.crm.helper.stown import get_access_token
from src.config import get_config
from src.redis_client import redis_client
from src.database import get_async_session
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from src.crm.stown.schemas import  ReadSFlat
from src.crm.stown.crud import upsert_flat
from fastapi.security.api_key import APIKey
from src.auth import get_api_key
from src.crm.stown.schemas import ReadSFlat, FilterSFlat, FilterSHouse

router_stown = APIRouter(
    prefix="/stown",
    tags=["Работа с внешними домами"]
)

conf = get_config()


@router_stown.get("/give-devices") 
async def get_devices_stown( 
        session: AsyncSession = Depends(get_async_session), 
        api_key: APIKey = Depends(get_api_key)

): 
     try:
        token = redis_client.get(conf.redis.STOWN_KEY)
        if not token:
            token = get_access_token()

        headers = {'Authorization': f'JWT {token}'}
        print(token)
        api_response = requests.get(conf.stown.DEVICES_URL, headers=headers)
        api_response.raise_for_status()
        return {
                "items": api_response.json(),
                "status": "success"
        }

     except Exception as e:
        await session.rollback()
        redis_client.delete(conf.redis.STOWN_KEY) 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
                "args": e.args if hasattr(e, 'args') else None,
            }
        )


@router_stown.get("/homes/{house_id}/give-flats")
async def get_flats_stown(
        house_id: int,
        session: AsyncSession = Depends(get_async_session),
        api_key: APIKey = Depends(get_api_key)
):
    try:
        url = conf.measures.HOMES_URL.format(house_id=house_id)
        headers = {
            "Authorization": f"Token {conf.measures.TOKEN}",
            "Accept": "application/json",
        }

        api_response = requests.get(
            url,
            headers=headers
            )

        if api_response.status_code != 200:
            raise Exception("Stown API error: " + api_response.text)

        data = api_response.json()
        saved = []
        for home in data: 
            try:
                home["house_id"] = house_id
                flat_in = ReadSFlat(**home) 
                saved_flat = await upsert_flat(session, flat_in, house_id)
                saved.append(saved_flat)
            except Exception as e:
                print(f"Ошибка обработки квартиры: {home}")
                print(e)

        return {
            "status": "success",
            "house_id": house_id,
            "saved": len(saved),
            "items": saved
        }

    except Exception as e:
        return {"error": str(e)}
 

@router_stown.get("/flats", response_model=Page[ReadSFlat])
async def get_flats(
    session: AsyncSession = Depends(get_async_session),
    api_key: APIKey = Depends(get_api_key),
    filters_params: FilterSFlat = Depends(),

):
    try:
        
        query = select(SFlat).where(SFlat.type == 'Квартира')
        if filters_params.house_id:
            query = query.filter(SFlat.house_id == filters_params.house_id)
        if filters_params.number:
            query = query.filter(SFlat.number == filters_params.number)
            
        return await paginate(session, query)
        

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "args": str(e),  
            }
        )