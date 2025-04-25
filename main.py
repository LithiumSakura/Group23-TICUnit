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
    gate_counts = crowd_detection.count_people_at_gates()
    print("#######################")
    print(gate_counts)
    if request.method == 'POST':
        return jsonify({"count": int(gate_counts)})
    return render_template('traffic.html', counts=gate_counts)

if __name__ == "__main__":
    app.run(debug=True)