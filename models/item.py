from dataclasses import dataclass
from typing import Optional
from playwright.sync_api import Locator


@dataclass
class Item:
    element: Locator
    title: Optional[str] = None
    rating: Optional[float] = None
    total_price: Optional[int] = None

    def __str__(self):
        return f"Title: {self.title},\n Price: {self.total_price} ₪,\n Rating: {self.rating}"
