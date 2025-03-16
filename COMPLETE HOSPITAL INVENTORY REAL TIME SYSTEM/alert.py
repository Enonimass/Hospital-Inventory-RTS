import smtplib
from email.message import EmailMessage
import sqlite3
from tkinter import messagebox

class SendEmail:
    def __init__(self, db_name="pharmacy.db"):
        # Connect to the database
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def check_low_quantity(self, threshold=10):
        """Check for drugs with quantity below the specified threshold and send an email alert."""
        """Display drugs running low on stock (less than 10 units)"""
        self.cursor.execute("SELECT name, quantity FROM drugs WHERE quantity < 10")
        low_stock_drugs = self.cursor.fetchall()

        if low_stock_drugs:
            # Format the list of low-stock drugs into a readable string
            low_stock_list = "\n".join([f"{name}: {quantity} units" for name, quantity in low_stock_drugs])

            # Prepare email content
            subject = "ALERT: Low Stock"
            body = f"The following drugs are running low:\n\n{low_stock_list}"
            receiver = 'youremail.com"

            # Send email alert
            self.email_alert(subject, body, receiver)
            messagebox.showinfo("Email Sent","Email Alert Sent Successfully")


    @staticmethod
    def email_alert(subject, body, to):
        """Send an email alert."""
        msg = EmailMessage()
        msg.set_content(body)
        msg['subject'] = subject
        msg['to'] = to
        user = "@gmail.com"  # Replace with your email
        msg['from'] = user
        password = "password"  # Replace with your email password

        try:
            # Connect to the SMTP server
            print("Connecting to SMTP server...")
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(user, password)
            print("Logged in successfully!")

            # Send the email
            server.send_message(msg)
            server.quit()
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")

    def close(self):
        """Close the database connection."""
        self.conn.close()


# Example usage
if __name__ == "__main__":
    email_sender = SendEmail()
    email_sender.check_low_quantity()  # Check for low stock and send email
    email_sender.close()  # Close the database connection