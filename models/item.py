class Item:
    def __init__(self, title=None, rate=None, total_price=None):
        self.title = title
        self.rate = rate
        self.total_price = total_price

    def __str__(self):
        return f"Title: {self.title}, Price: {self.total_price} ₪, Rating: {self.rate}"
