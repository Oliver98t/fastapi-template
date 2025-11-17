from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from typing import List
from database.connection import get_db
import database.schemas as schemas
from database.crud import item_crud, user_crud

class BaseRouter:
    def __init__(self, crud, model, input_model):
        self.crud = crud()
        self.model = model
        self.input_model = input_model
        self.router = APIRouter()
    # create default routes for basic crud functions
    def init_routes(self):
        singular_item = self.model.__tablename__[:-1]
        singular_item_slug = "/{"+ singular_item +"}"
        self.router.get("/", response_model=List[self.model])(self.get_all)
        self.router.get(singular_item_slug, response_model=self.model)(self.get)
        self.router.delete(singular_item_slug, response_model=self.model)(self.delete)
        # generate create route as input type cannot be detremined at runtime
        self.create = self.make_create_func(input_model=self.input_model, crud=self.crud)
        self.router.post("/", response_model=self.model)(self.create)

    def get_all(self, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        items = self.crud.get_all(db=db, skip=skip, limit=limit)
        return items

    def get(self, item_id: int, db: Session = Depends(get_db)):
        db_item = self.crud.get(db, id=item_id)
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return db_item

    def make_create_func(self, input_model, crud):
        def create(item, db: Session = Depends(get_db)):
            return crud.create(db=db, obj=item)
        # Set the correct annotation for FastAPI to use as input model
        create.__annotations__ = {'item': input_model, 'db': Session}
        return create

    def delete(self, item_id: int, db: Session = Depends(get_db)):
        db_item = self.crud.delete(db, id=item_id)
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return db_item

class ItemRouter(BaseRouter):
    def __init__(self):
        super().__init__(   crud=item_crud,
                            model=schemas.Item,
                            input_model=schemas.ItemInput)
        self.init_routes()

class UserRouter(BaseRouter):
    def __init__(self):
        super().__init__(   crud=user_crud,
                            model=schemas.User,
                            input_model=schemas.UserInput)
        self.init_routes()
        # example to add extra routes
        self.router.post("/", response_model=self.model)(self.create_user)

    def create_user(self, user: schemas.UserInput, db: Session = Depends(get_db)):
        email_user = self.crud.get_email(db=db, email=user.email)
        if email_user:
            raise HTTPException(status_code=404, detail="User exists")
        else:
            new_user = self.crud.create(db=db, obj=user)
            return new_user

item_routes = ItemRouter()
user_routes = UserRouter()