import smtplib
from email.message import EmailMessage

class SendEmail:
    @staticmethod
    def email_alert(subject, body, to):
        """Send an email alert when stock is low."""
        msg = EmailMessage()
        msg.set_content(body)
        msg['subject'] = subject
        msg['to'] = to
        user = "mailyatesting@gmail.com"  # Replace with your email
        msg['from'] = user
        password = "gcksanlbyrkxrwmm"  # Replace with your app password

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
