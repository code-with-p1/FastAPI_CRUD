from fastapi import APIRouter, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import AsyncSessionLocal, UserDB
from app.models.user import User
from typing import List
from uuid import UUID, uuid4

router = APIRouter()

@router.post("/users/", response_model=User)
async def create_user(user: User):
    async with AsyncSessionLocal() as session:
        db_user = UserDB(id=uuid4(), **user.dict(exclude={'id'}))
        session.add(db_user)
        try:
            await session.commit()
            await session.refresh(db_user)
            return db_user
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/", response_model=List[User])
async def get_users():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(UserDB))
        users = result.scalars().all()
        return users

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: UUID):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(UserDB).filter(UserDB.id == user_id))
        user = result.scalars().first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: UUID, user_update: User):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(UserDB).filter(UserDB.id == user_id))
        db_user = result.scalars().first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        for key, value in user_update.dict(exclude={'id'}, exclude_unset=True).items():
            setattr(db_user, key, value)
        try:
            await session.commit()
            await session.refresh(db_user)
            return db_user
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail=str(e))

@router.delete("/users/{user_id}")
async def delete_user(user_id: UUID):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(UserDB).filter(UserDB.id == user_id))
        user = result.scalars().first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        await session.delete(user)
        try:
            await session.commit()
            return {"message": "User deleted"}
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail=str(e))