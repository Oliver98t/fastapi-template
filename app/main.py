from fastapi import FastAPI
from routers.base import item_routes, user_routes

app = FastAPI(title="FastAPI Template Project", version="1.0.0")

app.include_router(item_routes.router, prefix="/items", tags=["items"])
app.include_router(user_routes.router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {"Server Status": "Running"}