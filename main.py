from flask import Flask, render_template, jsonify, request, Response
from crowd_counter import crowd_detection
import notification_system
import cv2
import time
import threading

app = Flask(__name__)

# Intialising the camera
camera = None
def get_camera():
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
    return camera

def release_camera():
    global camera
    if camera is not None:
        camera.release()
        camera = None

def generate_frames():
    cam = get_camera()
    while True:
        success, frame = cam.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
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
        
@app.route('/')
def landing():
    return render_template("index.html")

@app.route('/flights')
def flights():
    return render_template("flights.html")

@app.route('/traffic-count', methods=["GET","POST"])
def traffic_count():
    gate_counts = crowd_detection.count_people_at_gates()
    print(gate_counts)
    if request.method == 'POST':
        return jsonify({"count": int(gate_counts)})
    return render_template('traffic.html', counts=gate_counts)

@app.route('/camera_feed')
def camera_feed():
    return Response(generate_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/user-authentication')
def user_authentication():
    return render_template("user.html")

if __name__ == "__main__":
    threading.Thread(target=background_traffic_monitor,daemon=True).start()
    app.run(debug=True)