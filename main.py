from flask import Flask, render_template, jsonify, request, Response
from crowd_counter import crowd_detection
import notification_system
import time
import threading

app = Flask(__name__)
            
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
    return render_template("flights.html")

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