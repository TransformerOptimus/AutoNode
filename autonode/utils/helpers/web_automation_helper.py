import time
from PIL import Image


class WebAutomationHelper:

    def __init__(self):
        pass

    async def take_screenshot(self, page, path: str):
        await page.screenshot(path=path, timeout=600_000)
        return WebAutomationHelper().find_screenshot_size(path)

    def find_screenshot_size(self, path: str):
        img = Image.open(path)
        return img.size

    async def click_on_page(self, page, location: list, screenshot_size: tuple, click_count):
        if click_count == 1:
            await page.mouse.click(location[0] * (screenshot_size[0]), location[1] * (screenshot_size[1]), delay=100)
        elif click_count == 2:
            await page.mouse.dblclick(location[0] * (screenshot_size[0]), location[1] * (screenshot_size[1]))

        return float(location[0] * (screenshot_size[0])), float(location[1] * (screenshot_size[1]))

    async def type_str_on_page(self, page, text: str, system: str):
        if system == "Linux":
            await page.keyboard.type("AutoNode", delay=100)
            await page.keyboard.down('Control')
            await page.keyboard.press('A')
            await page.keyboard.up('Control')
            await page.keyboard.press('Backspace')

            await page.keyboard.type(text, delay=200)
        elif system == "mac":
            await page.keyboard.type("AutoNode", delay=100)
            await page.keyboard.down('Meta')
            await page.keyboard.press('A')
            await page.keyboard.up('Meta')
            await page.keyboard.press('Backspace')
            await page.keyboard.type(str(text), delay=200)

        time.sleep(1)
        await page.keyboard.press('Enter')

    async def type_multiple_elements_on_page(self, page, text_list: list, system: str, separation_key: str = "Enter"):
        if system == "Linux":
            await page.keyboard.type("AutoNode", delay=100)
            await page.keyboard.down('Control')
            await page.keyboard.press('A')
            await page.keyboard.up('Control')
            await page.keyboard.press('Backspace')
            for text in text_list:
                await page.keyboard.type(str(text), delay=200)
                time.sleep(2)
                await page.keyboard.press(separation_key)

        elif system == "mac":
            await page.keyboard.type("AutoNode", delay=100)
            await page.keyboard.down('Meta')
            await page.keyboard.press('A')
            await page.keyboard.up('Meta')
            await page.keyboard.press('Backspace')

            for text in text_list:
                await page.keyboard.type(str(text), delay=200)
                time.sleep(2)
                await page.keyboard.press(separation_key)
        time.sleep(1)
        await page.keyboard.press('Enter')
