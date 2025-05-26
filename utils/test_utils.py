from models.item import Item
from pages.search_page import SearchPage


def generate_search_with_random_dates(search_page: SearchPage, location: str, adults_count: int, children_count: int):
    search_page.set_location(location)
    search_page.set_random_dates()
    search_page.set_guests(adults=adults_count, children=children_count)
    search_page.click_on_search()


def open_item_in_new_tab(page, item: Item):
    with page.context.expect_page() as new_page_info:
        item.element.click()
    return new_page_info.value
