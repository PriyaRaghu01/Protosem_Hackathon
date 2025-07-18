import face_recognition
import cv2
import os
import pickle
import csv
import time
from datetime import datetime
from scapy.all import ARP, Ether, srp
import threading

# === Configuration ===
ENCODING_FILE = "encodings/faces.pkl"
EMPLOYEE_REGISTRY = "employee_registry.csv"
ATTENDANCE_FILE = "attendance_face.csv"
FINAL_RESULT_FILE = "final_attendance_status.csv"
IP_RANGE = "192.168.56.0/24"  # Set this to your Wi-Fi subnet

# === Load known face encodings ===
print("[INFO] Loading known face encodings...")
with open(ENCODING_FILE, "rb") as f:
    known_faces = pickle.load(f)

known_encodings = known_faces[0]
known_names = known_faces[1]

# === Load employee registry (MAC addresses) ===
employee_mac = {}
with open(EMPLOYEE_REGISTRY, "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        employee_mac[row[0]] = row[1]  # {name: MAC}

# === Helper function to log attendance ===
def log_attendance(name, status="Entered"):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time_now = now.strftime("%H:%M:%S")

    with open(ATTENDANCE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, date, time_now, status])

# === Wi-Fi MAC scanning ===
def scan_for_mac(target_mac):
    arp = ARP(pdst=IP_RANGE)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=0)[0]

    for sent, received in result:
        if received.hwsrc.lower() == target_mac.lower():
            return True
    return False

# === Wi-Fi monitoring thread ===
def monitor_wifi_logs(name, mac_address):
    print(f"[INFO] Starting Wi-Fi log checks for {name} ({mac_address})...")
    presence_count = 0

    for i in range(6):
        print(f"[INFO] Wi-Fi check {i+1}/6 in progress...")
        if scan_for_mac(mac_address):
            print(f"[INFO] {name} is present on the network.")
            presence_count += 1
        else:
            print(f"[WARNING] {name} not found on the network.")
        time.sleep(60)  # wait 1 minute between checks

    # === Final status based on Wi-Fi logs ===
    if presence_count == 6:
        final_status = "Present"
    else:
        final_status = "Absent"

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time_now = now.strftime("%H:%M:%S")
    print(f"[RESULT] {name} is marked as {final_status} based on Wi-Fi logs.")

    # Save final result
    with open(FINAL_RESULT_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, date, time_now, final_status])

# === Face Recognition + Attendance ===
print("[INFO] Starting face recognition...")
cap = cv2.VideoCapture(0)

recognized_names = set()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small)
    face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_match_index = face_distances.argmin()

        if matches[best_match_index]:
            name = known_names[best_match_index]

            if name not in recognized_names:
                recognized_names.add(name)
                log_attendance(name)

                # Delay Wi-Fi logging by 1 minute
                mac = employee_mac.get(name)
                if mac:
                    print(f"[INFO] Waiting for few minutes before connecting  Wi-Fi  {name}")
                    threading.Timer(60, monitor_wifi_logs, args=(name, mac)).start()
                else:
                    print(f"[ERROR] MAC address not found for {name}!")

        # Draw a rectangle and name
        top, right, bottom, left = [v * 4 for v in face_location]
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Face Recognition Attendance", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
