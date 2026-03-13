from app.scrapers.indeed_scraper import IndeedScraper

async def scrape_and_store_data(browser_manager):
    scraper = IndeedScraper(browser_manager)
    jobs = await scraper.scrape_jobs()
    print(f"len(jobs) jobs failed")
    return jobs