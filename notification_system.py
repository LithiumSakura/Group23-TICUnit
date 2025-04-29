import smtplib
from email.mime.text import MIMEText
from crowd_counter import crowd_detection

# Email Information
sender = "airportmanagementgroup23@gmail.com"

password = "bkpq alsr olqq mbfd" # Google app password
title = "Airport Management System Notification"
text = "This is a test notification for the email sender system that will be changed in the future"

def get_busy_gates(): # Returns a list of busy gates
    gate_traffic = crowd_detection.count_people_at_gates()
    busy_gates = []
    for i in range(len(gate_traffic)):
        if gate_traffic[i] >= 20:
            busy_gates.append(i+1)
    return busy_gates

def get_gates():
    return crowd_detection.count_people_at_gates()

def predict_traffic(old,new): # Returns a list of gates in which traffic is predicted to rise
    old_counts = old
    new_counts = new
    predicted_increases = []
    print("Starting check...")
    if len(old_counts) == len(new_counts):
        for i in range(len(old_counts)):
            if new_counts[i] >= old_counts[i]*1.2: # Checks for a 20% increase - can be changed!
                predicted_increases.append(new_counts[i])
    return predicted_increases

# MAKE AN AREA TO GRAB RECIPIENT INFO FROM DATABASE
# Once database is implemented this function will get the email of all users that have flights near a busy gate OR a flight that is soon to depart

# def get_passenger_info():
    return passengers











reciever = [sender, "samuelellisrobertson@gmail.com", "ben@woodwardfamily.eu", "oisinwillisdabomb@gmail.com", "pelayoanglada05@gmail.com"] # Change to program that gets based off gates


def make_notification(type,gate): # Type of notification and gate in which it involves (area can be none)
    if type.lower() == "crowd":
        return f"Warning - {gate} may be busy due to traffic."
    elif type.lower() == "reminder":
        return f"Reminder - your gate closes soon, please make your way to gate {gate}."
    
def send_email(title, text, sender, reciever, password):
    msg = MIMEText(text)
    msg["Subject"] = title
    msg["From"] = sender
    msg["To"] = ", ".join(reciever) # Adds all recievers of the message to the email
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp_server:
        smtp_server.starttls()
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, reciever, msg.as_string())
    print("Checkpoint - Sent!")


print(crowd_detection.count_all_images())
#send_email(title, text, sender, reciever, password)
