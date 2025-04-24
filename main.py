from flask import Flask, render_template, jsonify
from crowd_counter import crowd_detection

app = Flask(__name__)

@app.route('/')
def landing():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/traffic-count')
def traffic_count():
    count = crowd_detection.run_image_count("airportimage2.jpg")
    return jsonify({"count": int(count)})

if __name__ == "__main__":
    app.run(debug=True)