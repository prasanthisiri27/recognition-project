import cv2
import os
import numpy as np   # Needed to convert IDs to numpy array

# ----------------------------
# STEP 2: Dataset folder setup
# ----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "media/dataset")
MODEL_PATH = os.path.join(BASE_DIR, "media/model.yml")

# Create dataset folder if it doesn't exist
os.makedirs(DATASET_DIR, exist_ok=True)

# Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# ----------------------------
# Capture 50 face samples for an employee
# ----------------------------
def capture_face_samples(employee_id):
    cam = cv2.VideoCapture(0)
    count = 0

    employee_folder = os.path.join(DATASET_DIR, str(employee_id))
    os.makedirs(employee_folder, exist_ok=True)

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            count += 1
            face_img = gray[y:y+h, x:x+w]

            img_path = os.path.join(employee_folder, f"{count}.jpg")
            cv2.imwrite(img_path, face_img)

            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow("Capturing Faces", frame)

        if count >= 50:        # Stop after 50 images
            break
        if cv2.waitKey(1) == 27:  # ESC to exit
            break

    cam.release()
    cv2.destroyAllWindows()
    print(f"Captured {count} face images for employee {employee_id}.")

# ----------------------------
# Train LBPH model
# ----------------------------
def train_model():

    # Error handling if LBPH is missing
    if not hasattr(cv2.face, "LBPHFaceRecognizer_create"):
        print("ERROR: LBPHFaceRecognizer_create() is missing. Install opencv-contrib-python.")
        print("Run: pip install opencv-contrib-python")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    faces = []
    ids = []

    # Loop through dataset folders
    for folder in os.listdir(DATASET_DIR):
        folder_path = os.path.join(DATASET_DIR, folder)
        if not os.path.isdir(folder_path):
            continue

        for img_name in os.listdir(folder_path):
            img_path = os.path.join(folder_path, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue

            faces.append(img)
            ids.append(int(folder))

    if len(faces) == 0:
        print("No faces found in dataset. Skipping training.")
        return

    ids = np.array(ids, dtype=np.int32)
    recognizer.train(faces, ids)
    recognizer.save(MODEL_PATH)
    print("LBPH model trained and saved successfully.")
