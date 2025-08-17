from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database.db import SyncSessionLocal, UserDB
from app.models.user import User
from typing import List
from uuid import UUID, uuid4

router = APIRouter()

@router.post("/users/", response_model=User)
def create_user(user: User):
    with SyncSessionLocal() as session:
        db_user = UserDB(id=uuid4(), **user.dict(exclude={'id'}))
        session.add(db_user)
        try:
            session.commit()
            session.refresh(db_user)
            return db_user
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/", response_model=List[User])
def get_users():
    with SyncSessionLocal() as session:
        users = session.query(UserDB).all()
        return users

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: UUID):
    with SyncSessionLocal() as session:
        user = session.query(UserDB).filter(UserDB.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: UUID, user_update: User):
    with SyncSessionLocal() as session:
        db_user = session.query(UserDB).filter(UserDB.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        for key, value in user_update.dict(exclude={'id'}, exclude_unset=True).items():
            setattr(db_user, key, value)
        try:
            session.commit()
            session.refresh(db_user)
            return db_user
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=str(e))

@router.delete("/users/{user_id}")
def delete_user(user_id: UUID):
    with SyncSessionLocal() as session:
        user = session.query(UserDB).filter(UserDB.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        try:
            session.commit()
            return {"message": "User deleted"}
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=str(e))