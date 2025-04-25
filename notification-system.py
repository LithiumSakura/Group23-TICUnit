import smtplib
from email.mime.text import MIMEText

# Email Information
sender = "airportmanagementgroup23@gmail.com"

password = "bkpq alsr olqq mbfd" # Google app password
title = "Airport Management System Notification"
text = "This is a test notification for the email sender system that will be changed in the future"
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
    msg["To"] = ", ".join(reciever) # Adds all recievers of the message to the email
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp_server:
        smtp_server.starttls()
        print(password)
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, reciever, msg.as_string())
    print("Checkpoint - Sent!")

print(reciever)
send_email(title, text, sender, reciever, password)
