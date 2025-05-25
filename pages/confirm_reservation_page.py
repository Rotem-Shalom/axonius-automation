from datetime import datetime
from typing import Optional

from models.reservation_details import ReservationDetails
from pages.base_page import BasePage
import re

class ConfirmReservationPage(BasePage):
    DATE = '[data-section-id="DATE_PICKER"] .s1q42845'
    GUESTS_COUNT = '[data-section-id="GUEST_PICKER"] .s1q42845'
    PRICE_PARAMETERS = '.t6zyhla:not([data-testid="pd-title-TOTAL"])'
    PRICE_PARAMETERS_VALUE = '._1ur2ikp'
    TOTAL_PRICE = '[data-testid="price-item-total"]'
    PHONE_INPUT = '[name="phoneInputphone-login"]'

    def get_confirm_reservation_details(self):
        self.page.wait_for_timeout(1000)
        date = self.page.locator(self.DATE).text_content()
        guests_count = self.page.locator(self.GUESTS_COUNT).text_content().replace(r"\xa0", " ")
        price_parameters = [self.remove_float(val) for val in self.page.locator(self.PRICE_PARAMETERS).all_text_contents()]
        price_parameters_value = [self.remove_float(val) for val in self.page.locator(self.PRICE_PARAMETERS_VALUE).all_text_contents()]
        total_price_text = self.page.locator(self.TOTAL_PRICE).text_content()
        all_price_parameters = dict(zip(price_parameters, price_parameters_value))
        check_in, check_out = self.parse_checkin_checkout(date)
        total_price = self.remove_float(total_price_text)

        return ReservationDetails(
            check_in=check_in,
            check_out=check_out,
            guests_count=guests_count,
            price_parameters=all_price_parameters,
            total_price=total_price
        )

    @staticmethod
    def parse_checkin_checkout(date_str: str):
        """
        מקבלת מחרוזת תאריכים בפורמט:
        'May 25 – 26' או 'May 25 – 26' (עם רווחים מוזרים)
        ומחזירה check_in, check_out בפורמט 'day.month.year'
        """

        try:
            # מנקים תווים מיוחדים של רווחים או מקפים (en dash)
            date_str = date_str.replace('\u2009', '').replace('\u2013', '-').replace('–', '-').strip()
            # עכשיו אמור להיות בפורמט: 'May 25-26'

            # מפצלים לפי רווח ראשון: [month_str, days_range]
            parts = date_str.split(' ', 1)
            if len(parts) != 2:
                raise ValueError(f"Unexpected format: {date_str}")

            month_str, day_range = parts
            day_from, day_to = map(int, day_range.split('-'))

            current_year = datetime.now().year
            month_number = datetime.strptime(month_str, '%b' if len(month_str) == 3 else '%B').month

            check_in = datetime.strptime(f"{day_from}/{month_number}/{current_year}", "%d/%m/%Y")
            check_out = datetime.strptime(f"{day_to}/{month_number}/{current_year}", "%d/%m/%Y")

            return check_in, check_out
        except Exception as e:
            raise ValueError(f"Invalid date format '{date_str}': {e}")

    @staticmethod
    def remove_float(text: str):
        return re.sub(r'\.(\d+)', '', text)

    def enter_phone_number(self, phone_number: str):
        self.page.fill(self.PHONE_INPUT, phone_number)
