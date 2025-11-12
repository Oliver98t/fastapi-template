from fastapi import FastAPI
from routers import items, users
from database import engine

app = FastAPI(title="Simple FastAPI Project", version="1.0.0")

app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {"Server Status": "Running"}