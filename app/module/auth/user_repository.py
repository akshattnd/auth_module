from sqlalchemy.orm import Session
from app.module.auth.user_model import User
def get_user_by_email(db:Session, email:str):
    return db.query(User).filter(User.email == email).first() 

def create_user(db:Session, email:str, password_hash:str):
    user = User(
        email = email,
        password = password_hash,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user