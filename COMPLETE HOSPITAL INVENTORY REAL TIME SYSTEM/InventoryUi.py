import tkinter as tk
from tkinter import ttk, messagebox
from drugStore import PharmacyInventory  # Ensure this module contains your class
from alert import SendEmail

low_alert = SendEmail()

# Set up a consistent style using ttk.Style
def setup_style():
    style = ttk.Style()
    style.theme_use("clam")  # A modern, clean theme
    # Configure general style options
    style.configure(".", background="#ecf0f1", foreground="#2c3e50", font=("Helvetica", 11))
    # Style for TButton with a harmonious blue color
    style.configure("TButton", background="#3498db", foreground="white", padding=6)
    style.map("TButton",
              background=[('active', '#2980b9')],
              foreground=[('active', 'white')])

class PharmacyGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pharmacy Inventory Management")
        self.geometry("800x600")
        self.configure(bg="#ecf0f1")
        setup_style()

        # Create an instance of your inventory system
        self.pharmacy = PharmacyInventory()
        self.create_widgets()

    def create_widgets(self):
        # Notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Create three tabs: Manage, Inventory, and Low Stock
        self.manage_frame = ttk.Frame(self.notebook)
        self.inventory_frame = ttk.Frame(self.notebook)
        self.low_stock_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.manage_frame, text="Manage Inventory")
        self.notebook.add(self.inventory_frame, text="View Inventory")
        self.notebook.add(self.low_stock_frame, text="Low Stock")

        self.create_manage_tab()
        self.create_inventory_tab()
        self.create_low_stock_tab()

    def create_manage_tab(self):
        # Labels and entries for drug name and quantity
        ttk.Label(self.manage_frame, text="Drug Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.drug_name_entry = ttk.Entry(self.manage_frame, width=30)
        self.drug_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        ttk.Label(self.manage_frame, text="Quantity:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.quantity_entry = ttk.Entry(self.manage_frame, width=30)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Buttons for adding and deducting drugs
        add_btn = ttk.Button(self.manage_frame, text="Add Drug", command=self.add_drug)
        add_btn.grid(row=2, column=0, padx=10, pady=10)
        deduct_btn = ttk.Button(self.manage_frame, text="Deduct Drug", command=self.deduct_drug)
        deduct_btn.grid(row=2, column=1, padx=10, pady=10)

    def create_inventory_tab(self):
        # Treeview widget to display the full inventory
        columns = ("Name", "Quantity")
        self.inventory_tree = ttk.Treeview(self.inventory_frame, columns=columns, show='headings')
        self.inventory_tree.heading("Name", text="Drug Name")
        self.inventory_tree.heading("Quantity", text="Quantity")
        self.inventory_tree.column("Name", width=300)
        self.inventory_tree.column("Quantity", width=100)
        self.inventory_tree.pack(fill='both', expand=True, padx=10, pady=10)

        refresh_btn = ttk.Button(self.inventory_frame, text="Refresh Inventory", command=self.refresh_inventory)
        refresh_btn.pack(pady=10)

    def create_low_stock_tab(self):
        # Treeview widget to display low-stock drugs
        columns = ("Name", "Quantity")
        self.low_stock_tree = ttk.Treeview(self.low_stock_frame, columns=columns, show='headings')
        self.low_stock_tree.heading("Name", text="Drug Name")
        self.low_stock_tree.heading("Quantity", text="Quantity")
        self.low_stock_tree.column("Name", width=300)
        self.low_stock_tree.column("Quantity", width=100)
        self.low_stock_tree.pack(fill='both', expand=True, padx=10, pady=10)

        refresh_btn = ttk.Button(self.low_stock_frame, text="Refresh Low Stock", command=self.refresh_low_stock)
        refresh_btn.pack(pady=10)

        alert_btn = ttk.Button(self.low_stock_frame, text= "Send Alert" , command= low_alert.check_low_quantity )
        alert_btn.pack(pady=10)
        
    def add_drug(self):
        name = self.drug_name_entry.get().strip().lower()
        quantity_str = self.quantity_entry.get().strip()
        if not name or not quantity_str.isdigit():
            messagebox.showerror("Input Error", "Please enter a valid drug name and numeric quantity.")
            return

        quantity = int(quantity_str)
        self.pharmacy.add_drug(name, quantity)
        messagebox.showinfo("Success", f"Added {quantity} units of {name}.")
        self.drug_name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.refresh_inventory()
        self.refresh_low_stock()

    def deduct_drug(self):
        name = self.drug_name_entry.get().strip().lower()
        quantity_str = self.quantity_entry.get().strip()
        if not name or not quantity_str.isdigit():
            messagebox.showerror("Input Error", "Please enter a valid drug name and numeric quantity.")
            return

        quantity = int(quantity_str)
        self.pharmacy.deduct_drug(name, quantity)
        messagebox.showinfo("Success", f"Deducted {quantity} units of {name}.")
        self.drug_name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.refresh_inventory()
        self.refresh_low_stock()

    def refresh_inventory(self):
        # Clear and repopulate the inventory treeview
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        self.pharmacy.cursor.execute("SELECT * FROM drugs")
        drugs = self.pharmacy.cursor.fetchall()
        for drug in drugs:
            self.inventory_tree.insert("", tk.END, values=(drug[0], drug[1]))

    def refresh_low_stock(self):
        # Clear and repopulate the low stock treeview
        for item in self.low_stock_tree.get_children():
            self.low_stock_tree.delete(item)
        self.pharmacy.cursor.execute("SELECT name, quantity FROM drugs WHERE quantity < 10")
        drugs = self.pharmacy.cursor.fetchall()
        for drug in drugs:
            self.low_stock_tree.insert("", tk.END, values=(drug[0], drug[1]))

if __name__ == "__main__":
    app = PharmacyGUI()
    app.mainloop()
