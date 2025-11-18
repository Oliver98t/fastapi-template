from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from routers.base import item_routes, user_routes
from auth.auth import ( verify_password,
                        create_access_token,
                        get_current_user,
                        get_password_hash)

app = FastAPI(title="FastAPI Template Project", version="1.0.0")

app.include_router(item_routes.router, prefix="/items", tags=["items"])
app.include_router(user_routes.router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {"Server Status": "Running"}


# Dummy user for demonstration
test_user = {
    "username": "testuser",
    # Store the hashed password as a constant string (pre-hashed "testpassword")
    "hashed_password": "$5$rounds=535000$7hU3eq0bRPixOKGt$EZsO1jzHA7gfj6T4Ax2Co3nubhg1hvgqTw6WWIhbNM5"  # Replace with a real hash
}

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = test_user if form_data.username == test_user["username"] else None

    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected")
def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}!"}