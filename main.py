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


app = Flask(__name__)

load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")

flight_cache = {}
cache_timestamp = 0
CACHE_DURATION = 5 * 60
            
def background_traffic_monitor():
    last_count = crowd_detection.count_people_at_gates()
    while True:
        time.sleep(30) # Repeats every two minutes
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
        
@app.route('/', methods=["GET","POST"])
def landing():
    return render_template("index.html")

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

if __name__ == "__main__":
    threading.Thread(target=background_traffic_monitor,daemon=True).start()
    app.run(debug=True)