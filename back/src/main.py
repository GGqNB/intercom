
from typing import Dict
from fastapi import FastAPI, Form, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import asyncio
from fastapi.middleware.cors import CORSMiddleware
import threading
import json
from fastapi.security.api_key import APIKey



from src.auth import get_api_key
from src.config import API_KEY
from src.intercom_connect.router import router_intercom_connect
from src.crm.location.router import router_location
from src.crm.build.router import router_build
from src.crm.intercom.router import router_intercom

from src.intercom_connect.helpers import *

from fastapi_pagination import add_pagination


app = FastAPI(
   root_path="/api"
)

origins = [
    "http://localhost:9000",
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:9000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @router_user.post("",  status_code=status.HTTP_201_CREATED)
# async def add_user(
#     new_user: BaseUserSchemas,
#     session: AsyncSession = Depends(get_async_session),
# ):
#     try:
#         stmt = insert(User).values(new_user.model_dump()).returning(User)  # Возвращаем полную запись
#         result = await session.execute(stmt)
#         await session.commit()
#         created_user = result.scalar_one()  #

#         return {
#             "data" : created_user,
#             "status" : "success"
#         }  

#     except Exception as e:
#         await session.rollback() 
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail={
#                 "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": str(e), 
#                 "args": e.args if hasattr(e, 'args') else None,
#             }
#         )

app.include_router(router_intercom_connect)
app.include_router(router_location)
app.include_router(router_build)
app.include_router(router_intercom)
add_pagination(app)

