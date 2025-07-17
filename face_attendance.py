import cv2
import face_recognition
import pickle
import csv
import os
from datetime import datetime

# Load encoded faces
with open("encodings/faces.pkl", "rb") as f:
    known_encodings, known_names = pickle.load(f)

attendance_file = "attendance_face.csv"
today = datetime.now().strftime("%Y-%m-%d")

# Prevent duplicate marking
marked = set()
if os.path.exists(attendance_file):
    with open(attendance_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Date"] == today:
                marked.add(row["Name"])

# Initialize camera
cap = cv2.VideoCapture(0)

print("📸 Scanning for faces... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    for encoding, location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_encodings, encoding)
        face_distances = face_recognition.face_distance(known_encodings, encoding)
        best_match = min(range(len(matches)), key=lambda i: face_distances[i]) if matches else None

        if best_match is not None and matches[best_match]:
            name = known_names[best_match]
            top, right, bottom, left = [v * 4 for v in location]
            color = (0, 255, 0)

            # Display name on screen
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

            # Mark attendance
            if name not in marked:
                with open(attendance_file, "a", newline="") as f:
                    writer = csv.writer(f)
                    if os.stat(attendance_file).st_size == 0:
                        writer.writerow(["Name", "Date", "Time", "Status"])
                    writer.writerow([name, today, datetime.now().strftime("%H:%M:%S"), "Entered"])
                    print(f"✔ {name} marked as Entered")
                    marked.add(name)

    cv2.imshow("Face Recognition Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
