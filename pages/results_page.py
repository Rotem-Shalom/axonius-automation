from typing import List, Optional

from models.item import Item
import re
from pages.base_page import BasePage

class ResultsPage(BasePage):

    ITEM_SELECTOR = 'xpath=//*[@itemprop="itemListElement" and not(ancestor::*[contains(@class, "fqd7fl6")])]'
    NEXT_BUTTON = '[aria-label="Search results pagination"] [aria-label="Next"]'
    NEXT_BUTTON_DISABLED = '[aria-label="Search results pagination"] [aria-label="Next"][aria-disabled="true"]'
    RATE_SELECTOR = '.r4a59j5'
    TOTAL_PRICE = '.c1hpbaeu'
    TITLE = '.t1jojoys'
    PRICE_PER_HOUR = '.u1dgw2qm'

    def get_all_items(self):
        all_items = []

        while True:
            self.page.wait_for_timeout(3000)
            items = self.page.locator(self.ITEM_SELECTOR).all_text_contents()
            all_items.extend(self.define_item(item) for item in items)

            if self.page.locator(self.NEXT_BUTTON_DISABLED).count() > 0:
                break

            self.page.locator(self.NEXT_BUTTON).click()
        return all_items

    def define_item(self, item_data):
        clean_text = item_data.replace('\xa0', ' ').replace('\n', ' ').strip()

        title_match = re.match(r'([^,]+),', clean_text)
        title = title_match.group(1).strip() if title_match else None

        price_match = re.search(r'₪\s?(\d+)\s+total', clean_text)
        total_price = int(price_match.group(1)) if price_match else None

        rating_match = re.search(r'(\d\.\d{1,2}) out of 5|(\d\.\d{1,2}) \(\d+ reviews?\)', clean_text)
        rating_str = rating_match.group(1) or rating_match.group(2) if rating_match else None
        rating = float(rating_str) if rating_str else None

        return Item(title=title, rate=rating, total_price=total_price)

    @staticmethod
    def find_highest_rated_item(items: List[Item]) -> Optional[Item]:
        rated_items = [item for item in items if item.rate is not None]
        if not rated_items:
            return None
        return max(rated_items, key=lambda item: item.rate)

    @staticmethod
    def find_cheapest_item(items: list[Item]) -> Optional[Item]:
        return min(items, key=lambda item: item.total_price, default=None)

    def log_result_details(self, result):
        print(f"Title: {result['title']}")
        print(f"Price: {result['price']}")
        print(f"Rating: {result['rating']}")
