from app.db.session import get_db
from app.scrapers.core.browser import BrowserManager
from app.module.scraper_job.job_service import scrape_and_store_data
import asyncio
async def scrape_jobs():
    browser_manager = BrowserManager()
    db = next(get_db())
    await browser_manager.start(headless=False)
    jobs = await scrape_and_store_data(db, browser_manager)
    print (f"Total: {len(jobs)} scraped and store to db")
    if jobs:
        print(f"preview: {jobs[0]}")
    await browser_manager.close()

asyncio.run(scrape_jobs())