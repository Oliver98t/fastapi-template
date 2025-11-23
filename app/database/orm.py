from fastapi import APIRouter, HTTPException, Depends
from database.connection import get_db
from sqlmodel import Session, select
from .base_schemas import User
from .base_orm import base_crud
from .schemas import Item

class item_orm(base_crud):
    def __init__(self):
        super().__init__(Item)