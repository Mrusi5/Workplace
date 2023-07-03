
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
import aiohttp
from src.work.schemas import WorkplaceCreate
from src.work.models import workplace, post
from src.database import get_async_session


router = APIRouter(
    prefix="/workplace",
    tags=["workplace"]
)

async def get_workplace_by_id(workplace_id: int, session: AsyncSession = Depends(get_async_session)):
    workplace = await session.execute(select(workplace).where(workplace.c.id == workplace_id)).scalar()
    if not workplace:
        raise HTTPException(status_code=404, detail="Workplace not found")
    return workplace

#Поиск рабочей области
@router.get("/")
async def get_workplace(workplace_name: str, workplace_key: str, session: AsyncSession = Depends(get_async_session)):
    query = select(workplace).where(and_(workplace.c.key == workplace_key, workplace.c.name == workplace_name))
    result = await session.execute(query)
    record = result.fetchone()
    if record:
        return record._mapping
    else:
        raise HTTPException(status_code=404, detail="Workplace not found")

#Создание рабочей области
@router.post("/add")
async def add_workplace(new_workplace: WorkplaceCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(workplace).values(**new_workplace.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status":"success"}

#Удаление рабочей области
@router.delete("/{workplace_key}")
async def delete_workplace(workplace_name: str, workplace_key: str, session: AsyncSession = Depends(get_async_session)):
    query = select(workplace).where(and_(workplace.c.key == workplace_key, workplace.c.name == workplace_name))
    result = await session.execute(query)
    record = result.fetchone()
    if record:
        delete_query = workplace.delete().where(and_(workplace.c.key == workplace_key, workplace.c.name == workplace_name))
        await session.execute(delete_query)
        await session.commit()
        return {"status": "success"}
    else:
        raise HTTPException(status_code=404, detail="Workplace not found")

#Создание постов в рабочей области
@router.post("/posts")
async def create_post_with_workplace(title: str, description: str, workplace_name: str, workplace_key: str, session: AsyncSession = Depends(get_async_session)):
    async with aiohttp.ClientSession() as client_session:
        query = select(workplace).where(and_(workplace.c.key == workplace_key, workplace.c.name == workplace_name))
        result = await session.execute(query)
        record = result.fetchone()
        if record:
            post_data = dict()
            post_data["name"] = title
            post_data["description"] = description
            post_data["workplace_id"] = record.id
            post_data["date_create"] = datetime.utcnow()
            work = insert(post).values(**post_data)
            await session.execute(work)
            await session.commit()
            await client_session.post(url="https://example.com/send_notification", data={"message": "New post created!"})
            return {"status": "success"}

        else:
            raise HTTPException(status_code=404, detail="Workplace not found")

#Удаление постов
@router.delete("/posts/{post_id}")
async def delete_post(post_id: int, session: AsyncSession = Depends(get_async_session)):
    query = delete(post).where(post.c.id == post_id)
    result = await session.execute(query)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    await session.commit()
    return {"status": "success"}

#Обновление постов
@router.put("/posts/{post_id}")
async def update_post(post_id: int, title: str, description: str, session: AsyncSession = Depends(get_async_session)):
    query = update(post).where(post.c.id == post_id).values(name=title, description=description)
    result = await session.execute(query)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    await session.commit()
    return {"status": "success"}

#Поиск постов
@router.get("/posts/search")
async def search_posts(title: Optional[str] = None, workplace_name: Optional[str] = None, workplace_key: Optional[str] = None, session: AsyncSession = Depends(get_async_session)):
    query = select(post).join(workplace).where(post.c.workplace_id == workplace.c.id)
    if title:
        query = query.where(post.c.name.ilike(f"%{title}%"))
    if workplace_name:
        query = query.where(workplace.c.name == workplace_name)
    if workplace_key:
        query = query.where(workplace.c.key == workplace_key)
    result = await session.execute(query)
    records = result.fetchall()
    if not records:
        raise HTTPException(status_code=404, detail="No posts found")
    return [record._mapping for record in records]