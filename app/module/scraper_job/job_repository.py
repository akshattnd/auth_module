from sqlalchemy.orm import Session
from app.module.scraper_job.job_model import ScraperJob
def store_job(db:Session, job ):