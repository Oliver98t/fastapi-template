from sqlalchemy.orm import Session
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
        return db.query(self.table).filter(self.table.id == id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.table).offset(skip).limit(limit).all()
    
    def create(self, db: Session, obj):
        db_obj = self.table(**obj.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
        
    def delete(self, db: Session, id: int):
        db_user = db.query(self.table).filter(self.table.id == id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
        return db_user
    
class user_crud(base_crud):
    def __init__(self):
        super().__init__(DBUser, UserCreate)
    
    def get_email(self, db: Session, email: str):
        db_user = db.query(self.table).filter(self.table.email == email).first()
        return db_user

class item_crud(base_crud):
    def __init__(self):
        super().__init__(DBItem, ItemCreate)
