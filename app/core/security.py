from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, UTC

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str)-> str:
    return pwd_context.hash(password)

def verify_password(password:str, hashed:str):
    return pwd_context.verify(password, hashed)

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(hours=2)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)