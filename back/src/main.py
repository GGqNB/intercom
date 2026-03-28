from fastapi import FastAPI
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from src.factory.runners import monitor_intercoms, cleanup_task
from src.intercom_connect.router import cleanup_old_websockets, router_intercom_connect
from src.crm.location.router import router_location
from src.crm.build.router import router_build
from src.crm.intercom.router import router_intercom
from src.crm.logs.router import router_logs
from src.crm.helper.faker import router_fake
from src.crm.stown.router import router_stown
from src.crm.users.router import router_users
from src.intercom_connect.helpers import *
from fastapi_pagination import add_pagination
from fastapi.staticfiles import StaticFiles
from src.files.router import router_files


app = FastAPI(root_path="/api")

app.mount("/camera", StaticFiles(directory="src/files/camera"), name="camera")
# CORS
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

app.include_router(router_intercom_connect)
app.include_router(router_location)
app.include_router(router_build)
app.include_router(router_intercom)
app.include_router(router_logs)
app.include_router(router_fake)
app.include_router(router_stown)
app.include_router(router_files)
app.include_router(router_users)
add_pagination(app)






@app.on_event("startup")
async def startup_event():
    asyncio.create_task(cleanup_old_websockets())