
from sqlmodel import Session
from .schemas import DBUser, DBItem
from models.user import UserCreate
from models.item import ItemCreate

# TODO add delete to base crud
# base CRUD class
class base_crud():
    def __init__(self, table, model):
        self.table = table
        self.model = model

    # User CRUD operations

    def get(self, db: Session, id: int):
        return db.get(self.table, id)


    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        statement = self.table.select().offset(skip).limit(limit)
        results = db.exec(statement)
        return results.all()


    def create(self, db: Session, obj):
        db_obj = self.table(**obj.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


    def delete(self, db: Session, id: int):
        db_obj = db.get(self.table, id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj

class user_crud(base_crud):
    def __init__(self):
        super().__init__(DBUser, UserCreate)


    def get_email(self, db: Session, email: str):
        statement = self.table.select().where(self.table.email == email)
        result = db.exec(statement).first()
        return result

class item_crud(base_crud):
    def __init__(self):
        super().__init__(DBItem, ItemCreate)
