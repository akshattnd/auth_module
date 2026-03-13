from playwright.async_api import async_playwright

class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser = None
    
    async def start(self, headless = True):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)

    async def new_page(self):
        context = await self.browser.new_context()
        return await context.new_page()
    async def close(self):
        await self.browser.close()
        await self.playwright.stop()