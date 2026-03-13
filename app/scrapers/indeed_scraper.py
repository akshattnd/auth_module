from app.scrapers.core.base_scraper import BaseScraper

class IndeedScraper(BaseScraper):
    """<input aria-invalid="false" id="ifl-InputFormField-:passport-ssr-Reaktala:" name="__email" aria-required="true" type="email" autocomplete="email" autocorrect="off" autocapitalize="none" autofocus="" placeholder="youremail@email.com or 9876543210" class="passport-ssr-16cerhe e1jgz0i3" value="" fdprocessedid="axv9nd">"""
    BASE_URL = "https://in.indeed.com/"
    def __init__(self, browser_manager):
        super().__init__(browser_manager)
    async def scrape_jobs(self, qeury="backend developer", location = "Remote"):
        query = query.replace(" ", "+")
        
        url = f"{self.BASE_URL}/jobs?{query}&l={location}"
        
        await self.open(url)   
        
        await self.start()
        
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