from typing import Optional

from playwright.sync_api import Page, Locator


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def go_to(self, url: str):
        self.page.goto(url)

    def press_enter(self):
        self.page.keyboard.press("Enter")

    def press_escape(self):
        self.page.keyboard.press("Escape")

    def safe_text(self, item: Locator, selector: str, timeout: int = 1000) -> Optional[str]:
        try:
            return item.locator(selector).text_content(timeout=timeout)
        except:
            return None
