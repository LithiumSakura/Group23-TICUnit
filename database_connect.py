import pandas as pd
from datetime import datetime, timedelta

data = pd.read_csv("mock_flight_data.csv")

def get_emails_from_gate(gate):
    return data[data["Gate"]==gate]["Email"].tolist() # Returns a list of passenger emails depending on their gate

def get_email_from_id(id):
    result = data[data["ID"]==id]["Email"]

def get_departing_flight_info(): # Returns gates of passengers who's flights leave within 2 hours
    current_time = datetime.now().time()
    time_frame = (datetime.combine(datetime.today(),current_time) + timedelta(hours=2)).time()
    if current_time < time_frame:
        mask = (data["Departure"] >= current_time) & (data["Departure"] <= time_frame)
    else: # Would mean that an hour from the current time is past midnight
        mask = (data["Departure"] >= current_time) | (data["Departure"] <= time_frame)
    sorted_data = data[mask]
    gates = sorted_data["Gate"].tolist()
    return gates