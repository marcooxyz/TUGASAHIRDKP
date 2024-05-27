class Item:
    def __init__(self, name, category, quantity):
        self.name = name
        self.category = category
        self.quantity = quantity

    def __str__(self):
        return f"{self.name} ({self.category}): {self.quantity}"

    def add_quantity(self, amount):
        self.quantity += amount

    def remove_quantity(self, amount):
        if amount > self.quantity:
            raise ValueError("Not enough quantity to remove")
        self.quantity -= amount
        return self.quantity
