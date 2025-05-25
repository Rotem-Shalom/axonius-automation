from pages.base_page import BasePage
import time

class SearchPage(BasePage):
    LOCATION_INPUT = '.fp9kp52'
    SEARCH_PARAMETER = '.f1i5a5z'
    DAY_DATE = '.d11exu1w:not([aria-hidden="true"]):not([aria-disabled="true"])'
    ADD_GUESTS = '.fbb0tkq'
    STEPPER_ADULTS_INCREASE = '.piqlc25 [data-testid="stepper-adults-increase-button"]'
    STEPPER_CHILDREN_INCREASE = '.piqlc25 [data-testid="stepper-children-increase-button"]'
    SEARCH_BUTTON = '[data-testid="structured-search-input-search-button"]'
    SEARCH_RESULTS = 'div[itemscope]'


    def set_location(self, location: str):
        self.page.evaluate("window.scrollTo(0, 0)")
        self.page.fill(self.LOCATION_INPUT, location)
        self.page.keyboard.press("Enter")
        self.page.keyboard.press("Escape")

    def set_random_dates(self):
        self.page.evaluate("window.scrollTo(0, 0)")
        self.page.locator(self.SEARCH_PARAMETER, has_text="Check in").click()
        days = self.page.locator(self.DAY_DATE)
        days.first.click()
        self.page.keyboard.press("Escape")
        self.page.evaluate("window.scrollTo(0, 0)")
        self.page.locator(self.SEARCH_PARAMETER, has_text="Check out").click()
        days.nth(1).click()
        self.page.keyboard.press("Escape")

    def set_guests(self, adults=2, children=0):
        self.page.evaluate("window.scrollTo(0, 0)")
        self.page.click(self.ADD_GUESTS)
        for i in range(adults):
            self.page.click(self.STEPPER_ADULTS_INCREASE)
        for i in range(children):
            self.page.click(self.STEPPER_CHILDREN_INCREASE)

    def click_on_search(self):
        self.page.click(self.SEARCH_BUTTON)
        self.page.wait_for_selector(self.SEARCH_RESULTS)


