from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4

app = FastAPI(title="User CRUD API")

# Pydantic model for User
class User(BaseModel):
    id: Optional[UUID] = None
    name: str
    email: str
    age: int

# In-memory database
users_db = []

# Create
@app.post("/users/", response_model=User)
async def create_user(user: User):
    user.id = uuid4()
    users_db.append(user)
    return user

# Read all
@app.get("/users/", response_model=List[User])
async def get_users():
    return users_db

# Read one
@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: UUID):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# Update
@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: UUID, user_update: User):
    for index, user in enumerate(users_db):
        if user.id == user_id:
            updated_user = User(id=user_id, **user_update.dict(exclude={'id'}, exclude_unset=True))
            users_db[index] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

# Delete
@app.delete("/users/{user_id}")
async def delete_user(user_id: UUID):
    for index, user in enumerate(users_db):
        if user.id == user_id:
            users_db.pop(index)
            return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")