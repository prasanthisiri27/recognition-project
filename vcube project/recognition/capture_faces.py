import cv2
import os

# ✅ Correct path to media/dataset folder
dataset_path = os.path.join(os.path.dirname(__file__), '..', 'media', 'dataset')

# ✅ Create folder if it doesn't exist
os.makedirs(dataset_path, exist_ok=True)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Ask for employee ID
employee_id = input("Enter numeric Employee ID: ")

cap = cv2.VideoCapture(0)
count = 0

print("[INFO] Starting face capture. Look at the camera...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1
        filename = f"User.{employee_id}.{count}.jpg"
        filepath = os.path.join(dataset_path, filename)
        cv2.imwrite(filepath, gray[y:y+h, x:x+w])
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 2)

    cv2.imshow('Capturing Faces', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif count >= 50:
        break

print(f"[INFO] {count} samples captured for Employee ID {employee_id}")

cap.release()
cv2.destroyAllWindows()
