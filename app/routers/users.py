from fastapi import APIRouter, HTTPException
from typing import List
from models.user import User

router = APIRouter()

# Simple in-memory storage
users_db = []

@router.get("/", response_model=List[User])
def get_users():
    return users_db

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/", response_model=User)
def create_user(user: User):
    users_db.append(user)
    return user
