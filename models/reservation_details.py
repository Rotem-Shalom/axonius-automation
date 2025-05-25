from dataclasses import dataclass
from typing import Dict

@dataclass
class ReservationDetails:
    check_in: str
    check_out: str
    guests_count: int
    price_parameters: Dict[str, int]
    total_price: int

    def print_reservation_details(self):
        print("reservation details: \n"
              f"Check in : {self.check_in}\n"
              f"Check out : {self.check_out}\n"
              f"Guests count : {self.guests_count}\n"
              f"Price parameters : \n{self.price_parameters}\n"
              f"Total price : {self.total_price}\n")
