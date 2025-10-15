from sqlalchemy.orm import Session
from .models import DBUser, DBItem
from models.user import UserCreate
from models.item import ItemCreate


# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(DBUser).filter(DBUser.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(DBUser).filter(DBUser.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBUser).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    db_user = DBUser(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


# Item CRUD operations
def get_item(db: Session, item_id: int):
    return db.query(DBItem).filter(DBItem.id == item_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBItem).offset(skip).limit(limit).all()


def create_item(db: Session, item: ItemCreate):
    db_item = DBItem(name=item.name, price=item.price, is_active=item.is_active)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int):
    db_item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item