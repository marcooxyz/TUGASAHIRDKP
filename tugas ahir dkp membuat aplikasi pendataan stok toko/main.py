import tkinter as tk
from inventory_app import InventoryApp

def main():
    root = tk.Tk()
    iv = InventoryApp(root)
    iv.loop()

if __name__ == "__main__":
    main()
