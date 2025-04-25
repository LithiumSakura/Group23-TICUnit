import smtplib
from email.mime.text import MIMEText
import yagmail

# Email Information
sender = "airportmanagementgroup23@gmail.com"

password = "bkpq alsr olqq mbfd"
title = "Airport Notification"
text = "Test body"
reciever = [sender, "samuelellisrobertson@gmail.com"]


def make_notification(type,area): # Type of notification and area in which it involves (area can be none)
    if type.lower() == "crowd":
        return f"Warning - {area} may be busy due to traffic."
    elif type.lower() == "reminder":
        return f"Reminder - your gate closes soon, please make your way to gate {area}."
    
def send_email(title, text, sender, reciever, password):
    msg = MIMEText(text)
    msg["Subject"] = title
    msg["From"] = sender
    msg["To"] = ", ".join(reciever)
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp_server:
        smtp_server.starttls()
        print(password)
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, reciever, msg.as_string())
    print("Checkpoint - Sent!")

print(reciever)
send_email(title, text, sender, reciever, password)
