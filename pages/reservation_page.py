from pages.base_page import BasePage

class ReservationPage(BasePage):

    def get_reservation_details(self):
        # לקבל את פרטי ההזמנה המוצגים בצד ימין
        pass

    def click_reserve(self):
        self.page.click('button:has-text("Reserve")')

    def enter_phone_number(self, phone_number: str):
        self.page.fill('input[type="tel"]', phone_number)
