
from typing import AsyncGenerator
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, MetaData, String
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
Base = declarative_base()

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

metadata = MetaData()

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"
    
    id = Column("id", Integer, primary_key=True)
    username = Column("username", String, nullable=False)
    email = Column("email", String, nullable=False)
    hashed_password = Column("hashed_password", String, nullable=False)
    is_active = Column("is_active", Boolean, default=True, nullable=False)
    is_superuser = Column("is_superuser", Boolean, default=False, nullable=False)
    is_verified = Column("is_verified",Boolean, default=False, nullable=False)

class Workplace(Base):
    __tablename__ = "workplace"
    
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String, nullable=False)
    key = Column("key", String, nullable=False)   

class Post(Base):
    __tablename__ = "post"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String, nullable=False)
    description = Column("description", String)
    workplace_id = Column("workplace_id", String, ForeignKey('workplace.id', ondelete='CASCADE'), nullable=False)
    date_create = Column("date_create", TIMESTAMP, nullable=False)

