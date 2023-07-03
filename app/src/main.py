import asyncio
from fastapi import FastAPI
from src.auth.manager import get_user_manager
from src.auth.schemas import UserCreate, UserRead
from src.auth.base_config import auth_backend, fastapi_users
from src.work.router import router as router_work



app = FastAPI(
    title="Workplace"
)


#роутер из библиотеки fastapi_users для аунтефикации 
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)
#роутер из библиотеки fastapi_users для регистрации
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


#добавление роутеров из папки work
app.include_router(router_work)


