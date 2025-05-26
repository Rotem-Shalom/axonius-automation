from pages.base_page import BasePage
from utils import consts


class SearchPage(BasePage):
    LOCATION_INPUT_SELECTOR = '.fp9kp52'
    SEARCH_PARAMETER_SELECTOR = '.f1i5a5z'
    DAY_IN_CALENDAR_SELECTOR = '.d11exu1w:not([aria-hidden="true"]):not([aria-disabled="true"])'
    ADD_GUESTS_SELECTOR = '.fbb0tkq'
    ADULTS_INCREASE_SELECTOR = '.piqlc25 [data-testid="stepper-adults-increase-button"]'
    CHILDREN_INCREASE_SELECTOR = '.piqlc25 [data-testid="stepper-children-increase-button"]'
    SEARCH_BUTTON_SELECTOR = '[data-testid="structured-search-input-search-button"]'
    SEARCH_RESULTS_SELECTOR = 'div[itemscope]'

    def set_location(self, location: str):
        self.scroll_web_up()
        self.page.fill(self.LOCATION_INPUT_SELECTOR, location)
        self.press_enter()
        self.press_escape()

    def set_random_dates(self):
        self.scroll_web_up()
        self.page.locator(self.SEARCH_PARAMETER_SELECTOR, has_text=consts.CHECK_IN).click()
        days = self.page.locator(self.DAY_IN_CALENDAR_SELECTOR)
        days.first.click()
        self.press_escape()
        self.scroll_web_up()
        self.page.locator(self.SEARCH_PARAMETER_SELECTOR, has_text=consts.CHECK_OUT).click()
        days.nth(1).click()
        self.press_escape()

    def set_guests(self, adults=2, children=0):
        self.scroll_web_up()
        self.page.click(self.ADD_GUESTS_SELECTOR)
        for i in range(adults):
            self.page.click(self.ADULTS_INCREASE_SELECTOR)
        for i in range(children):
            self.page.click(self.CHILDREN_INCREASE_SELECTOR)

    def click_on_search(self):
        self.page.click(self.SEARCH_BUTTON_SELECTOR)
        self.page.wait_for_selector(self.SEARCH_RESULTS_SELECTOR)

    def scroll_web_up(self):
        self.page.wait_for_timeout(2000)
        self.page.evaluate("window.scrollTo(0, 0)")
