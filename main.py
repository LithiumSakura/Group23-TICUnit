from flask import Flask, render_template, jsonify, request, jsonify
from serpapi import GoogleSearch
from crowd_counter import crowd_detection
from dotenv import load_dotenv
from datetime import datetime, timedelta
import requests
import notification_system
import time
import threading
import os
import json
import re


app = Flask(__name__)

load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")
            
def background_traffic_monitor():
    last_count = crowd_detection.count_people_at_gates()
    while True:
        time.sleep(120) # Repeats every two minutes
        new_count = crowd_detection.count_people_at_gates()
        predicted_increases = notification_system.predict_traffic(last_count,new_count)
        for i in range(len(predicted_increases)):
            message = f"Traffic may be rising at gate number: {i+1}"
            notification_system.send_email(
                "Gate Traffic Notification",
                message,
                notification_system.sender,
                notification_system.reciever,
                notification_system.password
            )
        last_count = new_count

def background_flight_reminder():
    while True:
        time.sleep(300) # Refreshes every 5 mins
        # Add section here which checks database for flights leaving soon

def get_flight_info(flight_code):
    """Get flight info from API or fallback to sample data"""
    try:   
        url = "https://serpapi.com/search"
        params = {
            "api_key": SERP_API_KEY,
            "engine": "google_flights",
            "departure_id": "LHR",
            "arrival_id": "LAX",
            "outbound_date": datetime.now().strftime("%Y-%m-%d"),
            "return_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "travel_class": "1",
            "hl": "en",
            "gl": "us"
        }
        flight_data = []
        flights = []
        response = requests.get(url, params=params)
        results = response.json()
    
        if 'best_flights' in results:
            flights = results['best_flights']
        elif 'other_flights' in results:
            flights = results['other_flights']
        else:
            print("No available flights")
        
        for flight in flights:
            if flight.get("flights"):
                for f in flight.get("flights", []):
                    if f.get('flight_number') == flight_code:
                        flight_info = flight['flights'][0]
                        exact_match_found = True
                        flight_data.append({
                            "flight_id": flight_info.get('flight_number', flight_code),
                            "airline": flight_info.get('airline', 'Unknown Airline'),
                            "airline_logo": flight_info.get('airline_logo', ''),
                            "airplane": flight_info.get('airplane', 'Unknown Aircraft'),
                            "airport": flight_info.get('departure_airport', {}).get('name', 'Unknown'),
                            "departure_time": flight_info.get('departure_airport', {}).get('time', ''),
                            "destination": flight_info.get('arrival_airport', {}).get('name', 'Unknown'),
                            "arrival_time": flight_info.get('arrival_airport', {}).get('time', ''),
                            "duration": flight_info.get('duration', 0),
                            "travel_class": flight_info.get('travel_class', 'Economy'),
                            "status": "On Time"
                        })
                        # The regular expression 
                        break

            if exact_match_found:
                break

        return f"Here's your flight information:\n\n" \
                f"Flight: {flight_data[0]['flight_id']} ({flight_data[0]['airline']})\n" \
                f"Departure: {flight_data[0]['airport']}\n" \
                f"Destination: {flight_data[0]['destination']}\n" \
                f"Status: {flight_data[0]['status']}"
    
    except Exception as e:
        print(f"API Error: {str(e)}")
    if not flight_data:
        # Determine airline based on flight code prefix
        if flight_code.startswith("BA"):
            airline = "British Airways"
            departure = "London Heathrow"
            destination = "Los Angeles"
        elif flight_code.startswith("AA"):
            airline = "American Airlines"
            departure = "New York JFK"
            destination = "Chicago O'Hare"
        elif flight_code.startswith("UA"):
            airline = "United Airlines"
            departure = "San Francisco"
            destination = "Denver"
        elif flight_code.startswith("DL"):
            airline = "Delta Airlines"
            departure = "Atlanta"
            destination = "Seattle"
        else:
            airline = "Unknown Airline"
            departure = "Unknown Origin"
            destination = "Unknown Destination"
        
        flight_data.append({
            "flight_id": flight_code,
            "airline": airline,
            "airport": departure,
            "destination": destination,
            "status": "Unknown"
        })
        
        return f"Here's your flight information:\n\n" \
                f"Flight: {flight_data[0]['flight_id']} ({flight_data[0]['airline']})\n" \
                f"Departure: {flight_data[0]['airport']}\n" \
                f"Destination: {flight_data[0]['destination']}\n" \
                f"Status: {flight_data[0]['status']}"

def generate_response(message):
    """Generate a response based on user message""" 
    message = message.lower()
    flight_match = re.search(r'(?:flight\s+)?([a-z]{2}\d{1,4})', message, re.IGNORECASE) #TODO: Fix the regular expression the space in the flight code doesn't get the exact match just fallsback on the fake data
    # Check if the message is asking about flight information
    if flight_match:
        flight_code = flight_match.group(1).upper()
        return get_flight_info(flight_code)
    
    # If saying hello or similar greeting
    elif any(keyword in message for keyword in ['hi', 'hello', 'hey', 'greetings']):
        return "Hello! I'm your airport assistant. How can I help you with your flight today?"
    
    # If saying thanks
    elif any(keyword in message for keyword in ['thanks', 'thank you', 'thx']):
        return "You're welcome! Have a safe flight!"
    
    # Default response for other queries
    else:
        return "I can provide information about your flight or luggage. How can I assist you today?"
        
@app.route('/', methods=["GET","POST"])
def landing():
    user_message = ""
    bot_response = ""

    if request.method == 'GET':
        return render_template('index.html', user_message="", bot_response="", show_response=False)
    
    if request.method == 'POST':
        user_message = request.form.get('message', '').strip()
        
        if user_message:
            bot_response = generate_response(user_message)

    return render_template("index.html", user_message=user_message, bot_response=bot_response, show_response=(request.method == 'POST'))

@app.route('/flights', methods=["GET"])
def flights():
    
    params = {
        "api_key": SERP_API_KEY,
        "engine": "google_flights",
        "departure_id": "LHR",
        "arrival_id": "LAX",
        "outbound_date": datetime.now().strftime("%Y-%m-%d"),
        "return_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "travel_class": "1",
        "hl": "en",
        "gl": "us"
    }
    url = "https://serpapi.com/search"
    try:
        flight_data = []
        flights = []
        response = requests.get(url, params=params)
        results = response.json()
        if 'best_flights' in results:
            flights = results['best_flights']
        elif 'other_flights' in results:
            flights = results['other_flights']
        else:
            print("No available flights")         
            
        for flight in flights:
            if flight.get("flights"):
                flight_info = flight['flights'][0]
                flight_data.append({
                    "flight_id": flight_info.get('flight_number', 'N/A'),
                    "airline": flight_info.get('airline', 'Unknown Airline'),
                    "airline_logo": flight_info.get('airline_logo', ''),
                    "airplane": flight_info.get('airplane', 'Unknown Aircraft'),
                    "airport": flight_info.get('departure_airport', {}).get('name', 'Unknown'),
                    "departure_time": flight_info.get('departure_airport', {}).get('time', ''),
                    "destination": flight_info.get('arrival_airport', {}).get('name', 'Unknown'),
                    "arrival_time": flight_info.get('arrival_airport', {}).get('time', ''),
                    "duration": flight_info.get('duration', 0),
                    "travel_class": flight_info.get('travel_class', 'Economy'),
                    "status": "On Time"
                })

            if not flight_data:
                flight_data.append({
                    "flight_id": "BA123",
                    "airline": "British Airways",
                    "airline_logo": "",
                    "airplane": "Boeing 777",
                    "airport": "LHR",
                    "departure_time": "10:30 AM",
                    "destination": "Los Angeles",
                    "arrival_time": "1:45 PM",
                    "duration": 660,
                    "travel_class": "Economy",
                    "status": "Scheduled"
                })
                
    except Exception as err:
        print(f"Error fetching flight data: {str(err)}")
    
    return render_template("flights.html", flights=flight_data)

@app.route('/traffic-count', methods=["GET","POST"])
def traffic_count():
    gate_counts = crowd_detection.count_people_at_gates()
    print(gate_counts)
    if request.method == 'POST':
        return jsonify({"count": int(gate_counts)})
    return render_template('traffic.html', counts=gate_counts)

@app.route('/user-authentication')
def user_authentication():
    return render_template("user.html")

@app.route('/infoboard')
def infoboard():
    return render_template("infoboard.html")

if __name__ == "__main__":
    threading.Thread(target=background_traffic_monitor,daemon=True).start()
    app.run(debug=True)
