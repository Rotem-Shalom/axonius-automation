from pages.results_page import ResultsPage
from pages.search_page import SearchPage
import logging

logging.basicConfig(level=logging.INFO)

def test_airbnb_search(page):
    search_page = SearchPage(page)
    search_page.go_to("https://www.airbnb.com/")

    search_page.set_location("Tel Aviv")
    search_page.set_random_dates()
    search_page.set_guests(adults=2, children=0)
    search_page.click_on_search()

    results_page = ResultsPage(page)
    assert "Tel Aviv" in results_page.get_page_heading_text()

    items = results_page.get_all_items()
    highest_rate = results_page.find_highest_rated_item(items)
    min_price = results_page.find_cheapest_item(items)
    logging.info(f"items: {len(items)}")
    logging.info(f"Highest Rated Item: {highest_rate}")
    logging.info(f"Cheapest Item: {min_price}")
