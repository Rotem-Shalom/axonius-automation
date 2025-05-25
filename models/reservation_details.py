from dataclasses import dataclass
from datetime import datetime
from typing import Dict

@dataclass
class ReservationDetails:
    check_in: datetime
    check_out: datetime
    guests_count: str
    price_parameters: Dict[str, str]
    total_price: str

    def print_reservation_details(self):
        print("reservation details: \n"
              f"Check in : {self.check_in}\n"
              f"Check out : {self.check_out}\n"
              f"Guests count : {self.guests_count}\n"
              f"Price parameters : \n{self.price_parameters}\n"
              f"Total price : {self.total_price}\n")
