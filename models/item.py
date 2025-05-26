from dataclasses import dataclass
from typing import Optional
from playwright.sync_api import Locator


@dataclass
class Item:
    element: Locator
    title: Optional[str]
    rating: Optional[float]
    total_price: Optional[int]

    def __str__(self):
        return f"Title: {self.title},\n Price: {self.total_price} ₪,\n Rating: {self.rating}"
