
import cv2
import face_recognition
import numpy as np
import math
import os
import sys
import antispoofing.checker

def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'

class FaceRecognition:

    face_locations = []
    face_encodings = []
    face_names = []

    known_face_encodings = []
    known_face_names = []

    process_current_frame = True

    def __init__(self):
        self.encode_faces()

    def encode_faces(self):
        faces_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'faces')
        for image in os.listdir(faces_dir):
            face_image = face_recognition.load_image_file(faces_dir+'/'+image)
            face_encoding = face_recognition.face_encodings(face_image)[0]
            
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)

            print(self.known_face_encodings)

    def run_recognition(self):
        video_capture = cv2.VideoCapture(0)
        
        antispoofingdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'antispoofing')
        model_dir = antispoofingdir+'/resources/anti_spoof_models'  
        device_id = 0

        if not video_capture.isOpened():
            sys.exit("Could not open video device")

        while True:
            ret, frame = video_capture.read()

            if not ret:
                continue

            if self.process_current_frame:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                self.liveness_results = []

                for (top, right, bottom, left), face_encoding in zip(self.face_locations, self.face_encodings):
                    
                    # Scale back to original frame size
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                    # Extract the face for spoofing check
                    frame_h, frame_w = frame.shape[:2]
                    top = max(0, top)
                    bottom = min(frame_h, bottom)
                    left = max(0, left)
                    right = min(frame_w, right)

                    face_image = frame[top:bottom, left:right]
                    print(f"[DEBUG] Attempting to spoof check face of size {face_image.shape}")
                    
                    if face_image.size == 0 or face_image.shape[0] < 20 or face_image.shape[1] < 20:
                        print("[DEBUG] Face crop too small or empty, skipping spoof check.")
                        self.liveness_results.append(("UNKNOWN", (left, top, right, bottom)))
                        self.face_names.append("Unknown")
                        continue

                    spoof_result = antispoofing.checker.test(face_image, model_dir, device_id)
                    print(f"[DEBUG] Spoof detection result: {spoof_result}")

                    self.liveness_results.append((spoof_result, (left, top, right, bottom)))

                    if spoof_result == "REAL":
                        matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                        name = 'Unknown'
                        confidence = 'Unknown'

                        face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                        best_match_index = np.argmin(face_distances)

                        if matches[best_match_index]:
                            name = self.known_face_names[best_match_index]
                            confidence = face_confidence(face_distances[best_match_index])

                        name = name.split('.')[0]
                        display_name = f'{name} ({confidence})' if confidence != 'Unknown' else name
                    else:
                        display_name = "SPOOF DETECTED"

                    self.face_names.append(display_name)

            self.process_current_frame = not self.process_current_frame

            # Display results
            for (label, (left, top, right, bottom)), name in zip(self.liveness_results, self.face_names):
                color = (0, 255, 0) if label == "REAL" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, -1)
                display_text = f"{label}: {name}" if label != "REAL" else name
                cv2.putText(frame, display_text, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)

            cv2.imshow('Face Recognition + Anti-Spoofing', frame)

            if cv2.waitKey(1) == ord('a'):
                break

        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    face_recog_app = FaceRecognition()
    face_recog_app.run_recognition()

