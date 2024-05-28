import asyncio
import time
from playwright.async_api import async_playwright
from autonode.utils.helpers.web_automation_helper import WebAutomationHelper


class WebAutomationService:
    def __init__(self, url: str, system: str = "Linux"):
        self.loop = asyncio.get_event_loop()
        self.URL = url
        self.system = system
        self.screenshot_size = None

    async def initialise(self):
        await self._init_browser()
        await self.navigate_page(self.URL)

    async def navigate_page(self, url: str):
        await self.page.goto(url, timeout=600_000)

    async def take_screenshot(self, path: str):
        self.screenshot_size = await WebAutomationHelper().take_screenshot(self.page, path=path)
        return self.screenshot_size

    async def click_on_page(self, location: list, click_count: int = 1):
        click_location = await WebAutomationHelper().click_on_page(self.page, location, self.screenshot_size, click_count)
        return click_location

    async def download_on_click(self, location: list, download_path: str):
        time.sleep(2)
        async with self.page.expect_download(timeout=300_000) as download_info:
            await self.click_on_page(location)
        download = await download_info.value
        await download.save_as(download_path)

    async def type_on_page(self, text):
        if isinstance(text, list):
            await WebAutomationHelper().type_multiple_elements_on_page(self.page, text, self.system)
        elif isinstance(text, str):
            await WebAutomationHelper().type_str_on_page(self.page, text, self.system)
        else:
            raise ValueError(f"Invalid type for text. text type - {type(text)}")

    async def _init_browser(self):
        self.playwright = await async_playwright().start()
        firefox = self.playwright.firefox
        self.browser = await firefox.launch(headless=True, args=['--kiosk'])
        context = await self.browser.new_context(no_viewport=True,
                                                 viewport={"width": 1920, "height": 1080})

        self.page = await context.new_page()
        self.context = context

        await context.tracing.start(screenshots=True, snapshots=True, sources=True)

    async def stop_trace(self, job_dir):
        await self.context.tracing.stop(path=f"{job_dir}/trace.zip")

    async def close_browser(self):
        await self.browser.close()
        await self.playwright.stop()