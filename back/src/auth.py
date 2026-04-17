from fastapi import FastAPI, Depends, HTTPException, Header
# from src.config import settings
from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException
from starlette.status import HTTP_403_FORBIDDEN
from src.config import get_config

conf = get_config()
api_key_header = APIKeyHeader(name="authorization", auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == conf.security.API_KEY:
        return api_key_header   
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Go to auth"
        )
async def get_bot_key(bot_key_header: str = Security(api_key_header)):
    if bot_key_header == conf.security.BOT_KEY:
        return api_key_header   
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="no_bot_key"
        )        