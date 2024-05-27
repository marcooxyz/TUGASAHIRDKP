class Inventory:
    def __init__(self):
        self.categories = ["makanan manis", "makanan asin", "minuman" ,"alat mandi" ,"alat kebersihan rumah tangga"]
        self.stock = {category: {} for category in self.categories}

    def add_item(self, name, category, amount):
        if category not in self.categories:
            return False
        if name in self.stock[category]:
            self.stock[category][name] += amount
        else:
            self.stock[category][name] = amount
        return True

    def get_stock(self):
        return self.stock

    def take_out_item(self, category, name, amount):
        if category not in self.categories or name not in self.stock[category]:
            return False
        if self.stock[category][name] < amount:
            return False
        self.stock[category][name] -= amount
        if self.stock[category][name] == 0:
            del self.stock[category][name]
        return True
