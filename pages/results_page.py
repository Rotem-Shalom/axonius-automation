from typing import List, Optional

from models.item import Item
import re
from pages.base_page import BasePage

class ResultsPage(BasePage):

    ITEM_SELECTOR = '[itemprop="itemListElement"]'
    NEXT_BUTTON = '[aria-label="Search results pagination"] [aria-label="Next"]'
    NEXT_BUTTON_DISABLED = '[aria-label="Search results pagination"] [aria-label="Next"][aria-disabled="true"]'
    RATING_SELECTOR = '.r4a59j5'
    TOTAL_PRICE = '.c1hpbaeu'
    TITLE = '.t1jojoys'
    PRICE_PER_HOUR = '.u1dgw2qm'
    RESULTS_HEADING = '[data-testid="stays-page-heading"]'

    def get_all_items(self):
        all_items = []

        while True:
            self.page.wait_for_timeout(1000)
            items = self.page.locator(self.ITEM_SELECTOR).all()
            all_items.extend(self.define_item(item) for item in items)

            if self.page.locator(self.NEXT_BUTTON_DISABLED).count() == 0:
                break

            self.page.locator(self.NEXT_BUTTON).click()
        return all_items

    def define_item(self, item):
        try:
            title = item.locator(self.TITLE).text_content(timeout=5000)
        except:
            title = None

        try:
            rating = item.locator(self.RATING_SELECTOR).text_content(timeout=500)
            match = re.search(r'\d+\.\d+', rating)
            rating = float(match.group())
        except:
            rating = None

        try:
            total_price = item.locator(self.TOTAL_PRICE).text_content(timeout=500)
            match = re.search(r'₪\s*(\d+)', total_price)
            total_price = match.group(0)
        except:
            total_price = None

        return Item(element=item, title=title, rating=rating, total_price=total_price)

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
        return self.page.locator(self.RESULTS_HEADING).text_content()
