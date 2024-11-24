from fastapi import FastAPI, File, UploadFile
from facenet_pytorch import MTCNN
import tensorflow as tf
import numpy as np
from PIL import Image
from io import BytesIO
from fastapi.responses import JSONResponse, StreamingResponse
import cv2

app = FastAPI()

# Load TensorFlow model
model = tf.keras.models.load_model("model/expression_detection.h5")

# Emotion labels
emotion_labels = ["Angry", "Fear", "Happy", "Neutral", "Sad"]

# Initialize MTCNN from facenet-pytorch
detector = MTCNN(keep_all=True)  # `keep_all=True` to return all detected faces

@app.post("/detect-expression/")
async def detect_expression(file: UploadFile = File(...)):
    try:
        # Read and preprocess image
        contents = await file.read()
        image = Image.open(BytesIO(contents)).convert("RGB")

        # Detect faces using facenet-pytorch
        boxes, _ = detector.detect(image)
        if boxes is None or len(boxes) == 0:
            return JSONResponse({"error": "No faces detected."})

        # Convert image to numpy array for OpenCV processing
        image_np = np.array(image)

        for box in boxes:
            x1, y1, x2, y2 = map(int, box)

            # Crop the face
            face = image_np[y1:y2, x1:x2]

            # Preprocess the face for TensorFlow model
            face_gray = cv2.cvtColor(face, cv2.COLOR_RGB2GRAY)
            face_resized = cv2.resize(face_gray, (48, 48))
            face_normalized = face_resized / 255.0
            face_reshaped = np.reshape(face_normalized, (1, 48, 48, 1))

            # Predict expression
            predictions = model.predict(face_reshaped)
            emotion = emotion_labels[np.argmax(predictions)]

            # Draw bounding box and emotion label on the original image
            cv2.rectangle(image_np, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image_np, emotion, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Convert the processed image back to JPEG format
        _, buffer = cv2.imencode(".jpg", image_np)
        return StreamingResponse(BytesIO(buffer.tobytes()), media_type="image/jpeg")
    except Exception as e:
        return JSONResponse({"error": str(e)})