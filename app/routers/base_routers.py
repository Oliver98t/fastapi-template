from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from typing import List
from database.connection import get_db
from auth.encrypt import get_password_hash
import database.base_schemas as base_schemas
from database.base_orm import user_orm
from auth.encrypt import verify_password, create_access_token, get_admin_rights, get_read_write_rights

class BaseRouter:
    def __init__(self, orm, model, input_model):
        self.orm = orm()
        self.model = model
        self.input_model = input_model
        self.router = APIRouter()
    # create default routes for basic crud functions
    def init_routes(self, get_privilege, override_create=False):
        singular_item = self.model.__tablename__[:-1]
        singular_item_slug = "/{"+ singular_item +"}"
        self.router.get("/", response_model=List[self.model], dependencies=[Depends(get_privilege)])(self._get_all)
        self.router.get(singular_item_slug, response_model=self.model, dependencies=[Depends(get_privilege)])(self._get)
        self.router.delete(singular_item_slug, response_model=self.model, dependencies=[Depends(get_privilege)])(self._delete)
        # generate create route as input type cannot be determined at runtime
        if override_create == False:
            self.create = self._make_create_func(input_model=self.input_model, crud=self.orm)
            self.router.post("/", response_model=self.model, dependencies=[Depends(get_privilege)])(self.create)

    def _get_all(self, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        items = self.orm.get_all(db=db, skip=skip, limit=limit)
        return items

    def _get(self, item_id: int, db: Session = Depends(get_db)):
        db_item = self.orm.get(db=db, id=item_id)
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return db_item

    def _make_create_func(self, input_model, crud):
        def create(item, db: Session = Depends(get_db)):
            print("this here")
            return crud.create(db=db, obj=item)
        # Set the correct annotation for FastAPI to use as input model
        create.__annotations__ = {'item': input_model, 'db': Session}
        return create

    def _delete(self, item_id: int, db: Session = Depends(get_db)):
        db_item = self.orm.delete(db=db, id=item_id)
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return db_item

class UserRouter(BaseRouter):
    def __init__(self):
        super().__init__(   orm=user_orm,
                            model=base_schemas.User,
                            input_model=base_schemas.UserInput)

        self.init_routes(get_privilege=get_admin_rights, override_create=True)
        # example to add extra routes and set privileges
        self.router.post("/", response_model=self.model, dependencies=[Depends(get_admin_rights)])(self._create_user)
        self.router.post("/token")(self._login)

    def _create_user(   self,
                        user: base_schemas.UserInput,
                        db: Session = Depends(get_db)):

        email_user = self.orm.get_email(db=db, email=user.email)
        if email_user:
            raise HTTPException(status_code=404, detail="User exists")
        else:
            updated_user = base_schemas.UserInputHashed(
            username=user.username,
            email=user.email,
            privilege=user.privilege,
            hashed_password=get_password_hash(user.password)  # Example update
        )
            new_user = self.orm.create(db=db, obj=updated_user)
            return new_user

    # create new token for a user
    def _login(
        self,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
    ):
        user = self.orm.get_username(username=form_data.username, db=db)
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        encode_data =   {
                            "sub": user.username,
                            "priv": user.privilege

                        }
        access_token = create_access_token(data=encode_data)
        return {"access_token": access_token, "token_type": "bearer"}

user_routes = UserRouter()