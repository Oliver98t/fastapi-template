from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from database.schemas import UserPrivilege

# Secret key and algorithm for JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    print(to_encode)
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    username: str = payload.get("sub")
    privilige: int = payload.get("priv")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return privilige

def get_admin_rights(privilige: int = Depends(get_current_user)):
    if privilige > UserPrivilege.ADMIN.value:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return

def get_read_write_rights(privilige: int = Depends(get_current_user)):
    if privilige > UserPrivilege.READ_WRITE.value:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return

def get_read_rights(privilige: int = Depends(get_current_user)):
    if privilige > UserPrivilege.READ_ONLY.value:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return
