from typing import List
from sqlalchemy.orm import Session
from app.module.scraper_job.job_model import ScraperJob
from app.module.scraper_job.job_schema import JobSchema
def store_job(db:Session, job):
    scraper_job = ScraperJob(**job)
    db.add(scraper_job)
    db.commit()
    db.refresh(scraper_job)
    return scraper_job

def bulk_add_scraper_jobs(db:Session, jobs:List[any]):
    obj = [ScraperJob(**job) for job in jobs]
    db.bulk_save_objects(obj)
    db.commit()