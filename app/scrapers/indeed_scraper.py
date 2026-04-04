from app.scrapers.core.base_scraper import BaseScraper

class IndeedScraper(BaseScraper):
    """"""
    BASE_URL = "https://in.indeed.com"
    def __init__(self, browser_manager):
        super().__init__(browser_manager)
    async def scrape_jobs(self, qeury="backend developer", location = "Remote"):
        formated_query = qeury.replace(" ", "+")
    
        url = f"{self.BASE_URL}/jobs?{formated_query}&l={location}"
        await self.init_page()
        await self.open(url)
        
        jobs = await self.scrape()
        
        await self.close()
        return jobs
    
    async def scrape(self):

        job_cards = self.page.locator(".job_seen_beacon")
        count = await job_cards.count()
        jobs = []
        for i in range(count):
            card = job_cards.nth(i)
            job = await self.parse(card)
            jobs.append(job)
        return jobs

    async def parse(self, card):
        title = await card.locator("h2").text_content()
        company = await card.locator(".companyName").text_content()
        location = await card.locator(".companyLocation").text_content()
        link = await card.locator("a").get_attribute("href")
        return {
            "title": title,
            "company": company,
            "location": location,
            "link": link
        }