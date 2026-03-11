from sqlalchemy.orm import Session
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
) 

from . import user_repository

from app.module.auth.user_model import User

def register_user(db:Session, email:str, password:str):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise Exception("User already exists")
    password_hash = hash_password(password)
    user = user_repository.create_user(db, email, password_hash)
    return user
    
def login_user(db:Session, email:str, password:str):
    user = user_repository.get_user_by_email(db,email)
    
    if not user:
        raise Exception("Invalid credentials")
    if not verify_password(user.password, password):
        raise Exception("Invalid credentails")
    token = create_access_token({"sub":str(user.id)})
    return token