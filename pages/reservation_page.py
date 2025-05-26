from models.reservation_details import ReservationDetails
from pages.base_page import BasePage
from pages.confirm_reservation_page import ConfirmReservationPage
from utils.parsers import remove_float, remove_nonbreaking_spaces, format_date, extract_price_from_text


class ReservationPage(BasePage):
    SIDEBAR = '[data-section-id="BOOK_IT_SIDEBAR"]'
    PRICE_PER_NIGHT = '[data-section-id="BOOK_IT_SIDEBAR"] .u1dgw2qm'
    CHECK_IN = '[data-testid="change-dates-checkIn"]'
    CHECK_OUT = '[data-testid="change-dates-checkOut"]'
    GUESTS_COUNT = '#GuestPicker-book_it-trigger'
    PRICE_PARAMETERS = '.l1x1206l'
    PRICE_PARAMETERS_VALUE = '._1k4xcdh'
    TOTAL_PRICE = '._1qs94rc ._j1kt73'
    RESERVE_BUTTON = '[data-section-id="BOOK_IT_SIDEBAR"] [data-testid="homes-pdp-cta-btn"]'
    TRANSLATION_CLOSE_BUTTON = '[aria-label="Close"]'

    def get_reservation_details(self):
        self.page.wait_for_timeout(1000)
        check_in = format_date(self.page.locator(self.CHECK_IN).text_content())
        check_out = format_date(self.page.locator(self.CHECK_OUT).text_content())
        guests_count = remove_nonbreaking_spaces(self.page.locator(self.GUESTS_COUNT).text_content())
        total_price = extract_price_from_text(self.page.locator(self.TOTAL_PRICE).text_content())
        price_parameters_keys = [remove_float(val) for val in
                            self.page.locator(self.PRICE_PARAMETERS).all_text_contents()]
        price_parameters_values = [extract_price_from_text(val) for val in
                                  self.page.locator(self.PRICE_PARAMETERS_VALUE).all_text_contents()]
        price_parameters = dict(zip(price_parameters_keys, price_parameters_values))

        return ReservationDetails(check_in=check_in, check_out=check_out, guests_count=guests_count,
                                  price_parameters=price_parameters, total_price=total_price)

    def enter_on_reserve(self):
        self.page.click(self.RESERVE_BUTTON)
        return ConfirmReservationPage(self.page)

    def close_translation_window(self):
        self.page.wait_for_selector(self.TRANSLATION_CLOSE_BUTTON).click()
