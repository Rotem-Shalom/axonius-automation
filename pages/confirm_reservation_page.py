from models.reservation_details import ReservationDetails
from pages.base_page import BasePage

from utils.parsers import remove_float, parse_checkin_checkout, extract_price_from_text


class ConfirmReservationPage(BasePage):
    DATE_SELECTOR = '[data-section-id="DATE_PICKER"] .s1q42845'
    GUESTS_COUNT_SELECTOR = '[data-section-id="GUEST_PICKER"] .s1q42845'
    PRICE_PARAMETERS_SELECTOR = '.t6zyhla:not([data-testid="pd-title-TOTAL"])'
    PRICE_PARAMETERS_VALUE_SELECTOR = '._1ur2ikp'
    TOTAL_PRICE_SELECTOR = '[data-testid="price-item-total"]'
    PHONE_INPUT_SELECTOR = '[name="phoneInputphone-login"]'

    def get_confirm_reservation_details(self):
        self.page.wait_for_timeout(2000)
        check_in, check_out = parse_checkin_checkout(self.page.locator(self.DATE_SELECTOR).text_content())
        guests_count = self.page.locator(self.GUESTS_COUNT_SELECTOR).text_content()
        total_price = extract_price_from_text(self.page.locator(self.TOTAL_PRICE_SELECTOR).text_content())
        price_parameters_keys = [remove_float(val) for val in
                                 self.page.locator(self.PRICE_PARAMETERS_SELECTOR).all_text_contents()]
        price_parameters_values = [extract_price_from_text(val) for val in
                                   self.page.locator(self.PRICE_PARAMETERS_VALUE_SELECTOR).all_text_contents()]
        price_parameters = dict(zip(price_parameters_keys, price_parameters_values))

        return ReservationDetails(
            check_in=check_in,
            check_out=check_out,
            guests_count=guests_count,
            price_parameters=price_parameters,
            total_price=total_price
        )

    def enter_phone_number(self, phone_number: str):
        self.page.fill(self.PHONE_INPUT_SELECTOR, phone_number)
