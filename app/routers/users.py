from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from models.user import User, UserCreate
from database import get_db
from database import crud
from database.crud import user_crud

User_crud = user_crud()
router = APIRouter()

@router.get("/", response_model=List[User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = User_crud.get_all(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = User_crud.get(db=db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    email_user = User_crud.get_email(db=db, email=user.email)
    if email_user:
        raise HTTPException(status_code=404, detail="User exists")
    else:
        new_user = User_crud.create(db=db, obj=user)
        return new_user

@router.delete("/{user_id}", response_model=User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = User_crud.delete(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
