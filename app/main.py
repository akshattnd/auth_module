from fastapi import FastAPI
from app.module.auth.auth_route import router as auth_router
from app.common.response import ApiResponse
from app.db.base import Base
from app.db.session import engine
from contextlib import asynccontextmanager
app = FastAPI(
    title='Auth Api',
    debug=True,
    version="1.0.0",
    description="Authentication service"
)
@app.get("/",status_code=200)
def health_check():
    return ApiResponse(success=True,message="Ok")

app.include_router(auth_router)

@asynccontextmanager
async def lifespan(app:FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
