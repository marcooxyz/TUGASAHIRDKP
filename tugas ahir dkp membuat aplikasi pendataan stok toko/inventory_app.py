import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from inventory import Inventory

class InventoryApp:
    def __init__(self, root):
        self.inventory = Inventory()
        self.root = root
        self.root.title("Manajemen Stok Barang_fadhlanyuqa")
        
        # menentukan ukuran jendela 
        self.window_width = 800
        self.window_height = 600

        # untuk mengatur ukuran jendela yang akan diatur
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        
        # Membuat jendela tidak bisa diresize
        self.root.resizable(False, False)
        
        # Load gambar bg
        self.bg_image = Image.open("background.jpg")
        self.bg_image = self.bg_image.resize((self.window_width, self.window_height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Buat canvas bg
        self.canvas = tk.Canvas(self.root, width=self.window_width, height=self.window_height)
        self.canvas.pack(fill="both", expand=True)

        # Set bg img pada canvas 
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        
        self.create_widgets()

    def create_widgets(self):
        frame_width = 300
        frame_height = 150
        
        # Posisi frame untuk input barang
        self.input_frame = tk.Frame(self.canvas, bg='white', width=frame_width, height=frame_height)
        input_frame_x = (self.window_width - frame_width) // 2
        input_frame_y = 50
        self.canvas.create_window(input_frame_x, input_frame_y, window=self.input_frame, anchor='nw')

        tk.Label(self.input_frame, text="Tambah Barang Masuk", bg='white').grid(row=0, columnspan=2)
        tk.Label(self.input_frame, text="Nama Barang:", bg='white').grid(row=1, column=0)
        tk.Label(self.input_frame, text="Kategori:", bg='white').grid(row=2, column=0)
        tk.Label(self.input_frame, text="Jumlah:", bg='white').grid(row=3, column=0)

        self.name_entry = tk.Entry(self.input_frame)
        self.name_entry.grid(row=1, column=1)

        self.category_var = tk.StringVar(self.input_frame)
        self.category_var.set(self.inventory.categories[0])
        tk.OptionMenu(self.input_frame, self.category_var, *self.inventory.categories).grid(row=2, column=1)

        self.amount_entry = tk.Entry(self.input_frame)
        self.amount_entry.grid(row=3, column=1)

        tk.Button(self.input_frame, text="Tambah", command=self.add_stock, bg='green', fg='white').grid(row=4, columnspan=2, pady=5)

        # Posisi frame untuk melihat output stok
        self.output_frame = tk.Frame(self.canvas, bg='white', width=frame_width, height=frame_height)
        output_frame_x = (self.window_width - frame_width) // 2
        output_frame_y = 200
        self.canvas.create_window(output_frame_x, output_frame_y, window=self.output_frame, anchor='nw')

        tk.Button(self.output_frame, text="Tampilkan Stok", command=self.display_stock).grid(row=0, columnspan=2, pady=5)
        tk.Label(self.output_frame, text="Stok Barang Saat Ini", bg='white').grid(row=1, columnspan=2)
        self.stock_listbox = tk.Listbox(self.output_frame, width=50)
        self.stock_listbox.grid(row=2, column=0, columnspan=2)

        # Posisi frame untuk ambil barang
        self.takeout_frame = tk.Frame(self.canvas, bg='white', width=frame_width, height=frame_height)
        takeout_frame_x = (self.window_width - frame_width) // 2
        takeout_frame_y = 450 # Increase the y-coordinate to add more space between frames
        self.canvas.create_window(takeout_frame_x, takeout_frame_y, window=self.takeout_frame, anchor='nw')

        tk.Label(self.takeout_frame, text="Ambil Barang", bg='white').grid(row=0, columnspan=2)
        tk.Label(self.takeout_frame, text="Nama Barang:", bg='white').grid(row=1, column=0)
        tk.Label(self.takeout_frame, text="Kategori:", bg='white').grid(row=2, column=0)
        tk.Label(self.takeout_frame, text="Jumlah:", bg='white').grid(row=3, column=0)

        self.takeout_name_entry = tk.Entry(self.takeout_frame)
        self.takeout_name_entry.grid(row=1, column=1)

        self.takeout_category_var = tk.StringVar(self.takeout_frame)
        self.takeout_category_var.set(self.inventory.categories[0])
        tk.OptionMenu(self.takeout_frame, self.takeout_category_var, *self.inventory.categories).grid(row=2, column=1)

        self.takeout_amount_entry = tk.Entry(self.takeout_frame)
        self.takeout_amount_entry.grid(row=3, column=1)

        tk.Button(self.takeout_frame, text="Ambil", command=self.take_out_stock, bg='red', fg='white').grid(row=4, columnspan=2, pady=5)

    def add_stock(self):
        name = self.name_entry.get()
        category = self.category_var.get()
        try:
            amount = int(self.amount_entry.get())
            if amount < 0:
                raise ValueError
            if self.inventory.add_item(name, category, amount):
                messagebox.showinfo("Sukses", f"Berhasil menambah {amount} dari {name} ke kategori {category}")
                self.name_entry.delete(0, tk.END)
                self.amount_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Kategori tidak valid")
        except ValueError:
            messagebox.showerror("Error", "Jumlah harus berupa angka positif")

    def display_stock(self):
        self.stock_listbox.delete(0, tk.END)
        stock = self.inventory.get_stock()
        for category in self.inventory.categories:
            self.stock_listbox.insert(tk.END, f"Kategori: {category}")
            items = stock.get(category, {})
            if items:
                for item, amount in items.items():
                    self.stock_listbox.insert(tk.END, f"  {item}: {amount}")
            else:
                self.stock_listbox.insert(tk.END, "  Stok barang kosong")
            self.stock_listbox.insert(tk.END, "")

    def take_out_stock(self):
        name = self.takeout_name_entry.get()
        category = self.takeout_category_var.get()
        try:
            amount = int(self.takeout_amount_entry.get())
            if amount < 0:
                raise ValueError
            if self.inventory.take_out_item(category, name, amount):
                messagebox.showinfo("Sukses", f"Berhasil mengambil {amount} dari {name} dari kategori {category}")
                self.takeout_name_entry.delete(0, tk.END)
                self.takeout_amount_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Stok tidak mencukupi atau kategori tidak valid")
        except ValueError:
            messagebox.showerror("Error", "Jumlah harus berupa angka positif")

    def loop(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    app.loop()
