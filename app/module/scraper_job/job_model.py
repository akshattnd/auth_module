from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from app.db.base import Base
from sqlalchemy.sql import func

class ScraperJob(Base):
    __tablename__ = "scraper_jobs"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String,nullable=True)
    company = Column(String,nullable=True)
    location = Column(String,nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

