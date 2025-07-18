# Protosem_Hackathon
A prototype system that uses camera-based face detection and simulated Wi-Fi MAC logins on specific time periods to mark attendance automatically. 
# Face + Wi-Fi Attendance System

## 📌 Project Description
This is an IoT-enabled smart attendance system that combines face recognition and Wi-Fi connectivity to automate attendance marking. The system recognizes a person's face using a camera and verifies their presence on the network using MAC address scanning, ensuring accurate and real-time attendance logging.

## 🛠️ Features
- Face detection and recognition using `face_recognition` library
- Wi-Fi connectivity check using ARP scanning with `scapy`
- Automatic attendance marking to CSV files
- Detection of morning (FN) and afternoon (AN) presence
- MAC address mapping for user verification

## 🗂️ Modules
- `face_encoding.py`: Encodes known faces and stores them
- `face_recognition_module.py`: Detects and matches incoming faces
- `wifi_checker.py`: Scans network and identifies connected MAC addresses
- `attendance_updater.py`: Updates attendance based on face and MAC presence
- `mac_addresses.csv`: Maps names to registered MAC addresses
- `attendance.csv` & `final_attendance.csv`: Logs attendance data

## ⚙️ Installation & Requirements

```bash
pip install -r requirements.txt
```

`requirements.txt` should contain:
```
face_recognition
opencv-python
scapy
pickle-mixin
```

Ensure that `scapy` is installed to allow for ARP and Ether packet creation and sending.

## 🚀 How to Use

1. Add known face images to the `Images/` directory.
2. Run `encode_faces.py` to generate encodings.
3. Run the main script to start recognition and attendance marking:
```bash
python main.py
```
4. Attendance is logged in `attendance.csv` and `final_attendance.csv`.

## 📄 License
This project is licensed for educational and academic use only.

## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss.

## 🧠 Author
- Project by Team True Presence
