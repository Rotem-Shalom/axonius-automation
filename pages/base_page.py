from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def go_to(self, url: str):
        self.page.goto(url)

    def click(self, selector: str):
        self.page.click(selector)

    def type_text(self, selector: str, text: str):
        self.page.fill(selector, text)

    def wait_for_selector(self, selector: str):
        self.page.wait_for_selector(selector)
