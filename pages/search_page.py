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
        self.page.fill(self.LOCATION_INPUT, location)
        self.page.keyboard.press("Enter")
        self.page.keyboard.press("Escape")

    def set_random_dates(self):
        self.page.locator(self.SEARCH_PARAMETER, has_text="Check in").click()
        days = self.page.locator(self.DAY_DATE)
        days.first.click()
        self.page.keyboard.press("Escape")
        self.page.locator(self.SEARCH_PARAMETER, has_text="Check out").click()
        days.nth(1).click()
        self.page.keyboard.press("Escape")

    def set_guests(self, adults=2, children=0):
        self.page.click(self.ADD_GUESTS)
        for i in range(adults):
            self.page.click(self.STEPPER_ADULTS_INCREASE)
        for i in range(children):
            self.page.click(self.STEPPER_CHILDREN_INCREASE)

    def click_on_search(self):
        self.page.click(self.SEARCH_BUTTON)
        self.page.wait_for_selector(self.SEARCH_RESULTS)

    def get_results(self):
        return self.page.query_selector_all(self.SEARCH_RESULTS)

    def log_top_results(self):
        cards = self.page.locator(self.SEARCH_RESULTS)
        count = cards.count()
        if count == 0:
            print("No results found.")
            return

        # Find and log top-rated and cheapest
        cheapest_price = float("inf")
        highest_rating = 0
        cheapest_info = ""
        highest_info = ""

        for i in range(min(count, 20)):
            card = cards.nth(i)
            try:
                price = card.locator('[data-testid="price"]').text_content()
                price_num = int(''.join(filter(str.isdigit, price)))

                rating = card.locator('[aria-label*="rating"]').first.text_content()
                rating_num = float(rating) if rating else 0.0

                if price_num < cheapest_price:
                    cheapest_price = price_num
                    cheapest_info = f"Cheapest: {price} | Rating: {rating_num}"

                if rating_num > highest_rating:
                    highest_rating = rating_num
                    highest_info = f"Top Rated: {price} | Rating: {rating_num}"
            except:
                continue

        print(cheapest_info)
        print(highest_info)
