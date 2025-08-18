from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# JWT config
SECRET_KEY = os.getenv("SECRET_KEY", "changeme")
HR_USERNAME = os.getenv("HR_USERNAME", "admin")
HR_PASSWORD = os.getenv("HR_PASSWORD", "secret123")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def verify_password(plain: str, hashed_or_plain: str):
    """Verify plain text password against either plain or hashed value."""
    # For now HR_PASSWORD in .env is plain text, so allow direct comparison
    return plain == hashed_or_plain or pwd_context.verify(plain, hashed_or_plain)

def hash_password(password: str):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_hr(token: str = Depends(oauth2_scheme)):
    """Decode JWT and check if it's the configured HR."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or username != HR_USERNAME:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return {"username": HR_USERNAME}
