import sqlite3
from alert import SendEmail
from ImmediateAlert import SendEmail

SendEmail = SendEmail()

class PharmacyInventory:
    def __init__(self, db_name="pharmacy.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """Create the drugs table if it doesn't exist"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS drugs (
                name TEXT PRIMARY KEY,
                quantity INTEGER
            )
        ''')
        self.conn.commit()

    def add_drug(self, name, quantity):
        """Add a drug or update its quantity if it exists"""
        self.cursor.execute("SELECT quantity FROM drugs WHERE name = ?", (name,))
        result = self.cursor.fetchone()

        if result:
            new_quantity = result[0] + quantity
            # print(f"New Quantity : {new_quantity}")
            self.cursor.execute("UPDATE drugs SET quantity = ? WHERE name = ?", (new_quantity, name))
        else:
            self.cursor.execute("INSERT INTO drugs (name, quantity) VALUES (?, ?)", (name, quantity))
        
        self.conn.commit()
        print(f"{quantity} units of {name} added successfully!")
        if result:
            new_quantity = result[0] + quantity
            print(f"New Quantity : {new_quantity}")

    def deduct_drug(self, name, quantity):
        """Deduct quantity from an existing drug"""
        self.cursor.execute("SELECT quantity FROM drugs WHERE name = ?", (name,))
        result = self.cursor.fetchone()
        current_quantity = result[0]
        new_quantity = current_quantity - quantity

        if result:
            current_quantity = result[0]
            new_quantity = current_quantity - quantity

            if quantity > current_quantity:
                print(f"Error: Cannot deduct {quantity}, only {current_quantity} available.")
            else:
                new_quantity = result[0] - quantity
                self.cursor.execute("UPDATE drugs SET quantity = ? WHERE name = ?", (new_quantity, name))
                self.conn.commit()
                print(f"{quantity} units of {name} deducted successfully!")
                print(f"New Quantity : {new_quantity}")

                # Send alert if stock is low
                if new_quantity < 10 :
                    print(f"Running low on {name} : {new_quantity} units left. ")
                    subject = "ALERT: Low Stock Notification !"
                    body = f"{name} is running low : {new_quantity} units left. "
                    receiver = "@gmail.com"
                    SendEmail.email_alert(subject, body, receiver)


        else:
            print(f"Error: {name} not found in the database.")

    def display_drugs(self):
        """Display all drugs in the database"""
        self.cursor.execute("SELECT * FROM drugs")
        drugs = self.cursor.fetchall()

        if drugs:
            print("\nCurrent Drug Inventory:")
            for drug in drugs:
                print(f"Name: {drug[0]}, Quantity: {drug[1]}")
        else:
            print("\nNo drugs in the inventory.")

    def low_stock(self):
        """Display drugs running low on stock (less than 10 units)"""
        self.cursor.execute("SELECT name, quantity FROM drugs WHERE quantity < 10")
        low_stock_drugs = self.cursor.fetchall()

        if low_stock_drugs:
            SendEmail.check_low_quantity()
            print("\n⚠️ Running low on the following stocks:")
            for drug in low_stock_drugs:
                print(f"{drug[0]}: {drug[1]} units")
        else:
            print("\n✅ No stock running low.")

    def close(self):
        """Close the database connection"""
        self.conn.close()

if __name__ == "__main__":
    pharmacy = PharmacyInventory()
    
    while True:
        print("\n1. Add Drug")
        print("2. Deduct Drug")
        print("3. Show Inventory")
        print("4. Get Low Stock")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter drug name: ").strip().lower()
            try:
                quantity = int(input("Enter quantity to add: "))
                pharmacy.add_drug(name, quantity)
            except ValueError:
                print("Invalid input! Please enter a valid number.")
        elif choice == "2":
            name = input("Enter drug name: ").strip().lower()
            try:
                quantity = int(input("Enter quantity to deduct: "))
                pharmacy.deduct_drug(name, quantity)
            except ValueError:
                print("Invalid input! Please enter a valid number.")
        elif choice == "3":
            pharmacy.display_drugs()
        elif choice == "4":
            pharmacy.low_stock()
        elif choice == "5":
            print("Exiting program...")
            pharmacy.close()
            break
        else:
            print("Invalid choice! Please enter 1, 2, 3, 4, or 5.")
