"""
Create your custom routes from your own schemas here
"""

import database.schemas as schemas
from database.orm import item_orm
from auth.encrypt import get_read_write_rights
from routers.base_routers import BaseRouter


# separate new routers from the base
class ItemRouter(BaseRouter):
    def __init__(self):
        super().__init__(
            orm=item_orm(),
            model=schemas.Item,
            update_model=schemas.ItemUpdate,
            input_model=schemas.ItemInput,
        )
        self.init_routes(get_privilege=get_read_write_rights)


item_routes = ItemRouter()
