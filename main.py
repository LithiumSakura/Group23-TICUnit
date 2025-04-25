from flask import Flask, render_template, jsonify, request
from crowd_counter import crowd_detection

app = Flask(__name__)

@app.route('/')
def landing():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/traffic-count', methods=["GET","POST"])
def traffic_count():
    count = crowd_detection.run_image_count("airportimage2.jpg")
    if request.method == 'POST':
        return jsonify({"count": int(count)})
    return render_template('traffic.html', count=int(count))

if __name__ == "__main__":
    app.run(debug=True)