from fastapi import APIRouter, HTTPException, Depends
from fastapi.routing import APIRoute
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from typing import List
from database.connection import get_db
from auth.encrypt import get_password_hash
import database.base_schemas as base_schemas
from database.base_orm import user_orm, base_crud
from auth.encrypt import verify_password, create_access_token, get_admin_rights


class BaseRouter:
    def __init__(self, orm: base_crud, model, input_model, update_model):
        self.orm = orm
        self.model = model
        self.input_model = input_model
        self.update_model = update_model
        self.router = APIRouter()

    # create default routes for basic orm functions
    def init_routes(self, get_privilege):
        singular_item = self.model.__tablename__[:-1]
        self.singular_item_slug = "/{" + singular_item + "_id}"
        self.router.get(
            "/", response_model=List[self.model], dependencies=[Depends(get_privilege)]
        )(self._get_all)
        self.router.get(
            self.singular_item_slug,
            response_model=self.model,
            dependencies=[Depends(get_privilege)],
        )(self._get)
        self.router.delete(
            self.singular_item_slug,
            response_model=self.model,
            dependencies=[Depends(get_privilege)],
        )(self._delete)
        # generate update routes for put/patch as input type cannot be determined at runtime
        update = self._make_update_func(input_model=self.input_model, orm=self.orm)
        self.router.put(
            self.singular_item_slug,
            response_model=self.model,
            dependencies=[Depends(get_privilege)],
        )(update)
        patch = self._make_update_func(input_model=self.update_model, orm=self.orm)
        self.router.patch(
            self.singular_item_slug,
            response_model=self.model,
            dependencies=[Depends(get_privilege)],
        )(patch)

        # generate create route as input type cannot be determined at runtime
        create = self._make_create_func(input_model=self.input_model, orm=self.orm)
        self.router.post(
            "/", response_model=self.model, dependencies=[Depends(get_privilege)]
        )(create)

    def _get_all(self, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        items = self.orm.get_all(db=db, skip=skip, limit=limit)
        return items

    def _get(self, id: int, db: Session = Depends(get_db)):
        db_item = self.orm.get(db=db, id=id)
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return db_item

    def _make_create_func(self, input_model, orm):
        def create(item, db: Session = Depends(get_db)):
            return orm.create(db=db, obj=item)

        # Set the correct annotation for FastAPI to use as input model
        create.__annotations__ = {"item": input_model, "db": Session}
        return create

    def _make_update_func(self, input_model, orm):
        def update(id: int, item, db: Session = Depends(get_db)):
            return orm.update(db=db, id=id, obj=item)

        # Set the correct annotation for FastAPI to use as input model
        update.__annotations__ = {"id": int, "item": input_model, "db": Session}
        return update

    def _delete(self, id: int, db: Session = Depends(get_db)):
        db_item = self.orm.delete(db=db, id=id)
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return db_item

    def add_new_route(
        self, path: str, method: str, endpoint, response_model=None, get_privilege=None
    ):

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
            dependencies=dependencies,
            name=endpoint.__name__,
        )
        self.router.routes.append(new_route)


class UserRouter(BaseRouter):
    def __init__(self):
        super().__init__(
            orm=user_orm(),
            model=base_schemas.User,
            update_model=base_schemas.UserInputUpdate,
            input_model=base_schemas.UserInput,
        )

        self.init_routes(get_privilege=get_admin_rights)

        # example to add extra routes and set privileges
        self.add_new_route(
            path="/",
            method="POST",
            endpoint=self._create_user,
            response_model=self.model,
            get_privilege=get_admin_rights,
        )

        self.add_new_route(
            path=self.singular_item_slug,
            method="PUT",
            endpoint=self._update_user,
            response_model=self.model,
            get_privilege=get_admin_rights,
        )

        self.add_new_route(
            path=self.singular_item_slug,
            method="PATCH",
            endpoint=self._update_user,
            response_model=self.model,
            get_privilege=get_admin_rights,
        )

        self.add_new_route(path="/token", method="POST", endpoint=self._login)

        print(self.router.routes)

    def _update_user(
        self,
        user_id: int,
        user: base_schemas.UserInputUpdate,
        db: Session = Depends(get_db),
    ):

        current_user = self.orm.get(id=user_id, db=db)
        if not current_user:
            raise HTTPException(status_code=404, detail="User doesn't exist")

        # Get update data, excluding unset fields
        update_data = user.model_dump(exclude_unset=True)

        # Only hash password if it's provided
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(
                update_data.pop("password")
            )

        # Create update object with only provided fields
        updated_user = base_schemas.UserInputHashed(
            username=update_data.get("username", current_user.username),
            email=update_data.get("email", current_user.email),
            privilege=update_data.get("privilege", current_user.privilege),
            hashed_password=update_data.get(
                "hashed_password", current_user.hashed_password
            ),
        )

        new_user = self.orm.update(id=user_id, db=db, obj=updated_user)
        return new_user

    def _create_user(self, user: base_schemas.UserInput, db: Session = Depends(get_db)):

        username_user = self.orm.get_username(db=db, username=user.username)
        if username_user:
            raise HTTPException(status_code=404, detail="User exists")
        else:
            updated_user = base_schemas.UserInputHashed(
                username=user.username,
                email=user.email,
                privilege=user.privilege,
                hashed_password=get_password_hash(user.password),  # Example update
            )
            new_user = self.orm.create(db=db, obj=updated_user)
            return new_user

    # create new token for a user
    def _login(
        self,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
    ):
        user = self.orm.get_username(username=form_data.username, db=db)
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )
        encode_data = {"sub": user.username, "priv": user.privilege}
        access_token = create_access_token(data=encode_data)
        return {"access_token": access_token, "token_type": "bearer"}

user_routes = UserRouter()