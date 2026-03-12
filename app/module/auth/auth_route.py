from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.module.auth.user_schema import UserCreate, UserResponse
from app.module.auth import auth_service
from app.common.response import ApiResponse
from app.module.auth.auth_schema import (
    LoginRequest,
    TokenResponse
)
from app.module.auth.auth_dependencies import get_current_user
from app.module.auth.user_model import User
router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=ApiResponse[UserResponse], status_code=201)
def register(user:UserCreate, db:Session = Depends(get_db)):
    data =  auth_service.register_user(db,user.email,user.password)
    return ApiResponse(
        success=True,
        message="user registered successfully",
        data=data,   
        )
    

@router.post("/login",status_code=200,response_model=ApiResponse[TokenResponse])
def login(data:LoginRequest, db:Session = Depends(get_db)):
    token = auth_service.login_user(db,data.email,data.password)
    data =  TokenResponse(access_token=token)
    return ApiResponse(
        success=True,
        message="user Login successfully",
        data=data,   
        )
@router.get("/me",status_code=200,response_model=ApiResponse[UserResponse])
def get_profile(current_user:User = Depends(get_current_user)):
    return ApiResponse(
        success=True,
        message='user profile fetched',
        data=current_user
    )
