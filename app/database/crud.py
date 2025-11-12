from sqlmodel import Session, select
from .schemas import User, Item

class base_crud:
    def __init__(self, table):
        self.table = table

    def get(self, db: Session, id: int):
        return db.get(self.table, id)

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        statement = select(self.table).offset(skip).limit(limit)
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
        super().__init__(User)

    def get_email(self, db: Session, email: str):
        statement = select(self.table).where(self.table.email == email)
        result = db.exec(statement).first()
        return result

class item_crud(base_crud):
    def __init__(self):
        super().__init__(Item)
