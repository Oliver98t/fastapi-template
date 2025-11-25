from fastapi import APIRouter, HTTPException, Depends
from fastapi.routing import APIRoute
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from typing import List
from database.connection import get_db
from auth.encrypt import get_password_hash
import database.base_schemas as base_schemas
from database.base_orm import user_orm
from auth.encrypt import verify_password, create_access_token, get_admin_rights

class BaseRouter:
    def __init__(self, orm, model, input_model):
        self.orm = orm()
        self.model = model
        self.input_model = input_model
        self.router = APIRouter()
    # create default routes for basic orm functions
    def init_routes(self, get_privilege):
        singular_item = self.model.__tablename__[:-1]
        self.singular_item_slug = "/{"+ singular_item +"_id}"
        self.router.get("/", response_model=List[self.model], dependencies=[Depends(get_privilege)])(self._get_all)
        self.router.get(self.singular_item_slug, response_model=self.model, dependencies=[Depends(get_privilege)])(self._get)
        self.router.delete(self.singular_item_slug, response_model=self.model, dependencies=[Depends(get_privilege)])(self._delete)
        # generate update route as input type cannot be determined at runtime
        self.update = self._make_update_func(input_model=self.input_model, orm=self.orm)
        self.router.put(self.singular_item_slug, response_model=self.model, dependencies=[Depends(get_privilege)])(self.update)
        # generate create route as input type cannot be determined at runtime
        self.create = self._make_create_func(input_model=self.input_model, orm=self.orm)
        self.router.post("/", response_model=self.model, dependencies=[Depends(get_privilege)])(self.create)

    def _get_all(self, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        items = self.orm.get_all(db=db, skip=skip, limit=limit)
        return items

    def _get(self, item_id: int, db: Session = Depends(get_db)):
        db_item = self.orm.get(db=db, id=item_id)
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return db_item

    def _make_create_func(self, input_model, orm):
        def create(item, db: Session = Depends(get_db)):
            print("this here")
            return orm.create(db=db, obj=item)
        # Set the correct annotation for FastAPI to use as input model
        create.__annotations__ = {'item': input_model, 'db': Session}
        return create

    def _make_update_func(self, input_model, orm):
        def update(item_id: int, item, db: Session = Depends(get_db)):
            return orm.update(db=db, id=item_id, obj=item)
        # Set the correct annotation for FastAPI to use as input model
        update.__annotations__ = {'item_id': int, 'item': input_model, 'db': Session}
        return update

    def _delete(self, item_id: int, db: Session = Depends(get_db)):
        db_item = self.orm.delete(db=db, id=item_id)
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return db_item

    def add_new_route(  self,
                        path: str,
                        method: str,
                        endpoint,
                        response_model=None,
                        get_privilege=None):

        # remove existing path and method
        for i, route in enumerate(self.router.routes):
            if path == route.path and method in route.methods:
                del self.router.routes[i]

        dependencies = None
        if get_privilege:
            dependencies = [Depends(get_privilege)]

        new_route = APIRoute(
            path=path,
            endpoint=endpoint,
            methods=[method],
            response_model=response_model,
            dependencies=dependencies
        )
        self.router.routes.append(new_route)

class UserRouter(BaseRouter):
    def __init__(self):
        super().__init__(   orm=user_orm,
                            model=base_schemas.User,
                            input_model=base_schemas.UserInput)

        self.init_routes(get_privilege=get_admin_rights)

        # example to add extra routes and set privileges
        self.add_new_route( path='/',
                            method='POST',
                            endpoint=self._create_user,
                            response_model=self.model,
                            get_privilege=get_admin_rights)

        self.add_new_route( path='/token',
                            method='POST',
                            endpoint=self._login)

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