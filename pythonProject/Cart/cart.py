import random
from model import f_and_b, electronics

class CartSystem:
    def __init__(self):
        self.etalase = [f_and_b, electronics]
        self.weights = [90, 10]
        self.cart = []

    def get_item(self) -> str:
        selected_categories = random.choices(self.etalase, weights=self.weights)
        return random.choice(selected_categories)

cart = []

print(cart)