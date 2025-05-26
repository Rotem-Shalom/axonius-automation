from models.reservation_details import ReservationDetails
from pages.base_page import BasePage
from pages.confirm_reservation_page import ConfirmReservationPage
from utils.parsers import remove_float, remove_nonbreaking_spaces, format_date, extract_price_from_text


class ReservationPage(BasePage):
    CHECK_IN_SELECTOR = '[data-testid="change-dates-checkIn"]'
    CHECK_OUT_SELECTOR = '[data-testid="change-dates-checkOut"]'
    GUESTS_COUNT_SELECTOR = '#GuestPicker-book_it-trigger'
    PRICE_PARAMETERS_SELECTOR = '.l1x1206l'
    PRICE_PARAMETERS_VALUE_SELECTOR = '._1k4xcdh'
    TOTAL_PRICE_SELECTOR = '._1qs94rc ._j1kt73'
    RESERVE_BUTTON_SELECTOR = '[data-section-id="BOOK_IT_SIDEBAR"] [data-testid="homes-pdp-cta-btn"]'
    TRANSLATION_CLOSE_BUTTON_SELECTOR = '[aria-label="Close"]'

    def get_reservation_details(self):
        self.page.wait_for_timeout(1000)
        check_in = format_date(self.page.locator(self.CHECK_IN_SELECTOR).text_content())
        check_out = format_date(self.page.locator(self.CHECK_OUT_SELECTOR).text_content())
        guests_count = remove_nonbreaking_spaces(self.page.locator(self.GUESTS_COUNT_SELECTOR).text_content())
        total_price = extract_price_from_text(self.page.locator(self.TOTAL_PRICE_SELECTOR).text_content())
        price_parameters_keys = [remove_float(val) for val in
                                 self.page.locator(self.PRICE_PARAMETERS_SELECTOR).all_text_contents()]
        price_parameters_values = [extract_price_from_text(val) for val in
                                   self.page.locator(self.PRICE_PARAMETERS_VALUE_SELECTOR).all_text_contents()]
        price_parameters = dict(zip(price_parameters_keys, price_parameters_values))

        return ReservationDetails(check_in=check_in, check_out=check_out, guests_count=guests_count,
                                  price_parameters=price_parameters, total_price=total_price)

    def enter_on_reserve(self):
        self.page.click(self.RESERVE_BUTTON_SELECTOR)
        return ConfirmReservationPage(self.page)

    # Closes the popup window
    def close_translation_window(self):
        try:
            button = self.page.wait_for_selector(self.TRANSLATION_CLOSE_BUTTON_SELECTOR)
            if button.is_visible():
                button.click()
        except:
            pass
