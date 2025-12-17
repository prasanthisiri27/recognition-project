import cv2
import numpy as np
from PIL import Image
import os

# Paths (adjusted for recognition app location)
dataset_path = os.path.join(os.path.dirname(__file__), '..', 'dataset')
trainer_path = os.path.join(os.path.dirname(__file__), '..', 'trainer')

# Ensure trainer folder exists
if not os.path.exists(trainer_path):
    os.makedirs(trainer_path)

# Initialize recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def get_images_and_labels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    face_samples = []
    ids = []

    for image_path in image_paths:
        # Convert image to grayscale
        pil_img = Image.open(image_path).convert('L')
        img_numpy = np.array(pil_img, 'uint8')

        # Extract ID from filename (User.ID.sample.jpg)
        id = int(os.path.split(image_path)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)

        for (x, y, w, h) in faces:
            face_samples.append(img_numpy[y:y+h, x:x+w])
            ids.append(id)

    return face_samples, ids

print("[INFO] Training faces. Please wait...")

faces, ids = get_images_and_labels(dataset_path)
recognizer.train(faces, np.array(ids))

# Save the trained model
recognizer.write(os.path.join(trainer_path, "trainer.yml"))

print(f"[INFO] {len(np.unique(ids))} faces trained. Model saved at {trainer_path}/trainer.yml")
