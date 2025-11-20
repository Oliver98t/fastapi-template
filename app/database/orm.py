from fastapi import APIRouter, HTTPException, Depends
from database.connection import get_db
from sqlmodel import Session, select
from .schemas import User, Item

class base_crud:
    def __init__(self, table):
        self.table = table

    def get(self, id: int, db: Session = Depends(get_db)):
        return db.get(self.table, id)

    def get_all(self, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        statement = select(self.table).offset(skip).limit(limit)
        results = db.exec(statement)
        return results.all()

    def create(self, obj, db: Session = Depends(get_db)):
        db_obj = self.table(**obj.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, id: int, db: Session = Depends(get_db)):
        db_obj = db.get(self.table, id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj

class user_orm(base_crud):
    def __init__(self):
        super().__init__(User)

    def get_email(self, email: str, db: Session = Depends(get_db)):
        statement = select(self.table).where(self.table.email == email)
        result = db.exec(statement).first()
        return result

    def get_username(self, username: str, db: Session = Depends(get_db)):
        statement = select(self.table).where(self.table.username == username)
        result = db.exec(statement).first()
        return result

class item_orm(base_crud):
    def __init__(self):
        super().__init__(Item)
