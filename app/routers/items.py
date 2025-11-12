from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from typing import List
from database import get_db
from database.schemas import Item
from database.crud import item_crud

Item_crud = item_crud()
router = APIRouter()

@router.get("/", response_model=List[Item])
def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = Item_crud.get_all(db=db, skip=skip, limit=limit)
    return items

@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    db_item = Item_crud.get(db, id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.post("/", response_model=Item)
def create_item(item: Item, db: Session = Depends(get_db)):
    return Item_crud.create(db=db, obj=item)

@router.delete("/{item_id}", response_model=Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = Item_crud.delete(db, id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item