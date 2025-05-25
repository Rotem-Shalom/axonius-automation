from datetime import datetime
from typing import Optional
import re

from models.reservation_details import ReservationDetails
from pages.base_page import BasePage
from pages.confirm_reservation_page import ConfirmReservationPage


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

    def get_reservation_details(self):
        self.page.wait_for_timeout(1000)
        check_in = self.page.locator(self.CHECK_IN).text_content()
        formatted_check_in = datetime.strptime(check_in, "%m/%d/%Y")
        check_out = self.page.locator(self.CHECK_OUT).text_content()
        formatted_check_out = datetime.strptime(check_out, "%m/%d/%Y")
        guests_count = self.page.locator(self.GUESTS_COUNT).text_content().replace("\xa0", " ")
        price_parameters = [self.remove_float(val) for val in self.page.locator(self.PRICE_PARAMETERS).all_text_contents()]
        price_parameters_value = [self.remove_float(val) for val in self.page.locator(self.PRICE_PARAMETERS_VALUE).all_text_contents()]
        total_price_text = self.page.locator(self.TOTAL_PRICE).text_content()
        all_price_parameters = dict(zip(price_parameters, price_parameters_value))
        total_price = self.remove_float(total_price_text)

        return ReservationDetails(check_in=formatted_check_in, check_out=formatted_check_out, guests_count=guests_count, price_parameters=all_price_parameters, total_price=total_price)

    def enter_on_reserve(self):
        self.page.click(self.RESERVE_BUTTON)
        return ConfirmReservationPage(self.page)

    @staticmethod
    def remove_float(text: str):
        return re.sub(r'\.(\d+)', '', text)
