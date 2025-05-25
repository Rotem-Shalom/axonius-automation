from pages.reservation_page import ReservationPage
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


def test_airbnb_search2(page):
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
    with page.context.expect_page() as new_page_info:
        highest_rate.element.click()
    new_page = new_page_info.value
    reservation_page = ReservationPage(new_page)
    reservation_details = reservation_page.get_reservation_details()
    reservation_details.print_reservation_details()
    confirm_page = reservation_page.enter_on_reserve()
    confirm_reservation_details = confirm_page.get_confirm_reservation_details()
    print(confirm_reservation_details.price_parameters)
    assert reservation_details == confirm_reservation_details
    confirm_page.enter_phone_number('546876567')

