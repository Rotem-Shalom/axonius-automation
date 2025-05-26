import pytest

from pages.reservation_page import ReservationPage
from pages.results_page import ResultsPage
from pages.search_page import SearchPage
import logging

from utils import consts
from utils.test_utils import generate_search_with_random_dates, open_item_in_new_tab

logging.basicConfig(level=logging.INFO)


class TestAirbnb:
    @pytest.fixture
    def setup_search(self, page):
        search_page = SearchPage(page)
        search_page.go_to(consts.AIRBNB_WEB_ADDRESS)
        generate_search_with_random_dates(search_page=search_page, location=consts.TEST_CITY,
                                          adults_count=2,children_count=0)
        return ResultsPage(page)

    def test_airbnb_search(self, setup_search):
        results_page = setup_search
        assert consts.TEST_CITY in results_page.get_page_heading_text()
        items = results_page.get_all_items()
        logging.info(f"Highest Rated Item: {results_page.find_highest_rated_item(items)}")
        logging.info(f"Cheapest Item: {results_page.find_cheapest_item(items)}")

    def test_airbnb_search2(self, setup_search, page):
        results_page = setup_search
        assert consts.TEST_CITY in results_page.get_page_heading_text()
        highest_rate = results_page.find_highest_rated_item(results_page.get_all_items())
        reservation_page = ReservationPage(open_item_in_new_tab(page=page, item=highest_rate))
        reservation_page.close_translation_window()
        reservation_details = reservation_page.get_reservation_details()
        reservation_details.print_details()
        confirm_page = reservation_page.enter_on_reserve()
        confirm_reservation_details = confirm_page.get_confirm_reservation_details()
        print(reservation_page)
        print(confirm_reservation_details)
        assert reservation_details == confirm_reservation_details
        confirm_page.enter_phone_number('546876567')
