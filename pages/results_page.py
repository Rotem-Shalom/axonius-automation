from typing import List, Optional

from playwright.sync_api import Locator

from models.item import Item
from pages.base_page import BasePage
from utils.parsers import extract_float_from_text, extract_price_from_text


class ResultsPage(BasePage):
    ITEM_SELECTOR = '[itemprop="itemListElement"]'
    NEXT_BUTTON_SELECTOR = '[aria-label="Search results pagination"] [aria-label="Next"]'
    NEXT_BUTTON_DISABLED_SELECTOR = '[aria-label="Search results pagination"] [aria-label="Next"][aria-disabled="true"]'
    RATING_SELECTOR = '.r4a59j5'
    TOTAL_PRICE_SELECTOR = '.c1hpbaeu'
    TITLE_SELECTOR = '.t1jojoys'
    RESULTS_HEADING_SELECTOR = '[data-testid="stays-page-heading"]'

    def get_all_items(self):
        all_items = []

        while True:
            self.page.wait_for_timeout(1000)
            self.page.wait_for_selector(self.ITEM_SELECTOR)
            items = self.page.locator(self.ITEM_SELECTOR).all()
            all_items.extend(self.define_item(item) for item in items)

            if self.page.locator(self.NEXT_BUTTON_DISABLED_SELECTOR).is_visible():
                break

            self.page.locator(self.NEXT_BUTTON_SELECTOR).click()
        return all_items

    @staticmethod
    def find_highest_rated_item(items: List[Item]) -> Optional[Item]:
        rated_items = [item for item in items if item.rating is not None]
        if not rated_items:
            return None
        return max(rated_items, key=lambda item: item.rating)

    @staticmethod
    def find_cheapest_item(items: list[Item]) -> Optional[Item]:
        priced_items = [item for item in items if item.total_price is not None]
        if not priced_items:
            return None
        return min(priced_items, key=lambda item: item.total_price)

    def get_page_heading_text(self):
        return self.page.locator(self.RESULTS_HEADING_SELECTOR).text_content()

    def define_item(self, item: Locator) -> Item:
        title = self.safe_text(item, self.TITLE_SELECTOR)
        rating_text = self.safe_text(item, self.RATING_SELECTOR)
        total_price_text = self.safe_text(item, self.TOTAL_PRICE_SELECTOR)

        rating = extract_float_from_text(rating_text) if rating_text else None
        total_price = extract_price_from_text(total_price_text) if total_price_text else None

        return Item(element=item, title=title, rating=rating, total_price=total_price)
