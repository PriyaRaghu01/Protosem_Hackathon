
import face_recognition
import os
import pickle

dataset_path = r"C:\Users\priya\Downloads\FACE RECOGNITION Final\FACE_RECOGNITION\Images"

encoding_file = "encodings/faces.pkl"

# ✅ Create the encodings directory if it doesn't exist
os.makedirs(os.path.dirname(encoding_file), exist_ok=True)

known_encodings = []
known_names = []

for filename in os.listdir(dataset_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image = face_recognition.load_image_file(os.path.join(dataset_path, filename))
        encoding = face_recognition.face_encodings(image)
        if encoding:
            known_encodings.append(encoding[0])
            name = os.path.splitext(filename)[0]
            known_names.append(name)

with open(encoding_file, "wb") as f:
    pickle.dump((known_encodings, known_names), f)

print("✅ Face encodings saved.")

