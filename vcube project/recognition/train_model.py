import cv2
import os
import numpy as np
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def train_model():
    dataset_path = os.path.join(BASE_DIR, "media", "dataset")

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    face_samples = []
    ids = []

    # Loop through all files in dataset folder
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith(".jpg"):
                path = os.path.join(root, file)
                img = Image.open(path).convert('L')  # grayscale
                img_np = np.array(img, 'uint8')

                # Extract ID from filename: User.ID.sample.jpg
                filename = os.path.split(file)[-1]
                parts = filename.split(".")
                if len(parts) >= 4 and parts[1].isdigit():
                    id = int(parts[1])
                    face_samples.append(img_np)
                    ids.append(id)

    if len(face_samples) == 0:
        print("[ERROR] No training data found in dataset folder.")
        return

    recognizer.train(face_samples, np.array(ids))

    # Ensure trainer folder exists
    trainer_path = os.path.join(BASE_DIR, "recognition", "trainer")
    os.makedirs(trainer_path, exist_ok=True)

    model_path = os.path.join(trainer_path, "model.yml")
    recognizer.write(model_path)
    print(f"[INFO] Model training completed and saved at {model_path}")

# Example usage:
if __name__ == "__main__":
    train_model()
