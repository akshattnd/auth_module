from sqlalchemy.orm import Session
from app.scrapers.indeed_scraper import IndeedScraper
from app.module.scraper_job.job_repository import bulk_add_scraper_jobs
async def scrape_and_store_data(db:Session, browser_manager):
    scraper = IndeedScraper(browser_manager)
    jobs = await scraper.scrape_jobs()
    if jobs:
        bulk_add_scraper_jobs(db, jobs)
    return jobs