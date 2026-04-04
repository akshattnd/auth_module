import asyncio

from app.scrapers.core.base_scraper import BaseScraper


class IndeedScraper(BaseScraper):
    """"""

    BASE_URL = "https://in.indeed.com"
    # Listings are div.job_seen_beacon (table-based card) inside the mosaic widget.
    JOB_MOSAIC = "#mosaic-provider-jobcards"
    JOB_CARD = f"{JOB_MOSAIC} div.job_seen_beacon"

    def __init__(self, browser_manager):
        super().__init__(browser_manager)

    NEXT_PAGE = 'a[data-testid="pagination-page-next"]'

    async def scrape_jobs(
        self,
        qeury="backend developer",
        location="Remote",
        max_pages: int = 20,
    ):
        formated_query = qeury.replace(" ", "+")
        location_param = location.replace(" ", "+")
        url = f"{self.BASE_URL}/jobs?q={formated_query}&l={location_param}"
        await self.init_page()
        await self.open(url)

        jobs = await self.scrape(max_pages=max_pages)

        await self.close()
        return jobs

    async def scrape(self, max_pages: int = 20):
        seen_links: set[str] = set()
        all_jobs: list[dict] = []

        for _ in range(max_pages):
            await self.page.wait_for_load_state("domcontentloaded")
            await self.page.wait_for_selector(
                self.JOB_CARD, state="attached", timeout=60_000
            )

            for job in await self._scrape_current_page():
                link = job.get("link")
                if not link or link in seen_links:
                    continue
                seen_links.add(link)
                all_jobs.append(job)

            next_loc = self.page.locator(self.NEXT_PAGE)
            if await next_loc.count() == 0:
                break
            href = await next_loc.first.get_attribute("href")
            if not href:
                break
            next_url = (
                href if href.startswith("http") else f"{self.BASE_URL}{href}"
            )
            await self.page.goto(next_url, wait_until="domcontentloaded")
            await asyncio.sleep(0.4)

        return all_jobs

    async def _scrape_current_page(self) -> list[dict]:
        job_cards = self.page.locator(self.JOB_CARD)
        total = await job_cards.count()
        out: list[dict] = []
        seen: set[str] = set()
        for i in range(total):
            card = job_cards.nth(i)
            if not await self._bring_card_into_view(card):
                continue
            job = await self.parse(card)
            if not job or not job.get("link"):
                continue
            if job["link"] in seen:
                continue
            seen.add(job["link"])
            out.append(job)
        return out

    async def _bring_card_into_view(self, card) -> bool:
        """Mosaic keeps hidden duplicate beacons; scroll_into_view alone can hang on invisible nodes."""
        try:
            await card.scroll_into_view_if_needed(timeout=4_000)
        except Exception:
            pass
        if await card.is_visible():
            return True
        await self.page.mouse.wheel(0, 600)
        await asyncio.sleep(0.2)
        try:
            await card.scroll_into_view_if_needed(timeout=3_000)
        except Exception:
            pass
        return await card.is_visible()

    async def parse(self, card):
        # Matches current Indeed card: h2.jobTitle > a.jcs-JobTitle > span[title]
        title = await self._first_text(
            card,
            [
                "h2.jobTitle a.jcs-JobTitle span[title]",
                "h2.jobTitle a span",
                "h2.jobTitle a.jcs-JobTitle",
                "h2.jobTitle a",
                "[data-testid='job-title']",
                "h2.jobTitle",
            ],
        )
        if not title:
            return None

        company = await self._first_text(
            card,
            [
                "[data-testid='company-name']",
                "span.companyName",
                ".companyName",
            ],
        )
        location = await self._first_text(
            card,
            [
                "[data-testid='text-location'] span",
                "[data-testid='text-location']",
                "div.company_location [data-testid='text-location']",
                "div.companyLocation",
                ".companyLocation",
            ],
        )
        link_loc = card.locator(
            "h2.jobTitle a.jcs-JobTitle, a.jcs-JobTitle[data-jk], h2.jobTitle a[data-jk]"
        ).first
        link = None
        if await link_loc.count():
            link = await link_loc.get_attribute("href", timeout=5_000)
            if link and link.startswith("/"):
                link = f"{self.BASE_URL}{link}"
        return {
            "title": title,
            "company": company,
            "location": location,
            "link": link,
        }

    async def _first_text(self, root, selectors: list[str], timeout_ms: int = 5_000):
        for sel in selectors:
            loc = root.locator(sel).first
            if await loc.count() == 0:
                continue
            try:
                text = await loc.text_content(timeout=timeout_ms)
                if text and text.strip():
                    return text.strip()
            except Exception:
                continue
        return None
