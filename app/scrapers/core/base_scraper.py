
class BaseScraper:
    def __init__(self, browser_manager):
        self.browser_manager = browser_manager
        self.page = None
    async def init_page(self):
        if not self.page:
            self.page = await self.browser_manager.new_page()            
    async def open(self, url):
        await self.page = self.init_page()
        await self.page.goto(url)

    def close(self):
        if self.page:
            self.page.close()
