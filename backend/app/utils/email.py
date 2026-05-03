import smtplib
import os
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_otp() -> str:
    """Generate a 6-digit OTP."""
    return str(random.randint(100000, 999999))

def send_otp_email(receiver_email: str, otp: str):
    """
    Sends an OTP to the provided email address using SMTP.
    Requires SMTP_EMAIL and SMTP_PASSWORD to be set in environment variables.
    """
    sender_email = os.environ.get("SMTP_EMAIL")
    sender_password = os.environ.get("SMTP_PASSWORD")

    if not sender_email or not sender_password:
        print(f"Warning: SMTP_EMAIL or SMTP_PASSWORD not configured. Mocking email to {receiver_email}. OTP: {otp}")
        return

    subject = "Your ClubHub Verification Code"
    body = f"""
    Hello,

    Welcome to ClubHub! 

    Your verification code is: {otp}

    Please enter this code on the verification page to activate your account.

    Thanks,
    The ClubHub Team
    """

    msg = MIMEMultipart()
    msg['From'] = f"ClubHub <{sender_email}>"
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print(f"OTP successfully sent to {receiver_email}")
    except Exception as e:
        print(f"Failed to send email to {receiver_email}. Error: {e}")
        # Optionally, raise the exception or handle it
