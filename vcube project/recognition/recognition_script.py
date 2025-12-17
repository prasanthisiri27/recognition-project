import os
import sys
import django
import cv2
from datetime import date

# --- Base directory (project root where manage.py lives) ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- Ensure project root is on sys.path ---
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# --- Django settings ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "face_recognition_system.settings")
django.setup()

# --- Import models ---
from employees.models import Employee
from attendance.models import Attendance



# --- Model path ---
MODEL_PATH = os.path.join(BASE_DIR, "recognition", "trainer", "model.yml")

# --- Haar cascade ---
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def mark_attendance():
    if not os.path.exists(MODEL_PATH):
        print(f"Model file not found at: {MODEL_PATH}")
        return
    else:
        print(f"Model file found at: {MODEL_PATH}")

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_PATH)

    cam = cv2.VideoCapture(0)
    print("Recognition started. Press 'q' to quit.")

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            label, confidence = recognizer.predict(roi)

            print(f"[DEBUG] Predicted ID={label}, Confidence={confidence:.2f}")

            display_text = f"Unknown ({confidence:.1f})"

            if confidence < 85:
                try:
                    emp = Employee.objects.get(id=label)
                    today = date.today()

                    if not Attendance.objects.filter(employee=emp, date=today).exists():
                        Attendance.objects.create(employee=emp, status='Present')
                        print(f"[ATTENDANCE] Marked Present for {emp.name} (ID {emp.id})")

                    display_text = f"{emp.name} ({confidence:.1f})"
                except Employee.DoesNotExist:
                    print(f"[ERROR] No Employee found with ID {label}")
            else:
                print("[INFO] Face detected but confidence too low")

            # Draw rectangle and overlay text
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, display_text, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    print("Recognition ended.")

# Run the function
if __name__ == "__main__":
    mark_attendance()
