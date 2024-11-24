from fastapi import FastAPI, File, UploadFile
from mtcnn import MTCNN
import tensorflow as tf
import numpy as np
import cv2
from io import BytesIO
from PIL import Image
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse

app = FastAPI()

# Load model
model = tf.keras.models.load_model("model/expression_detection.h5")

# Emotion labels
emotion_labels = ["Angry", "Fear", "Happy", "Neutral", "Sad"]

# Initialize MTCNN
detector = MTCNN()

@app.post("/detect-expression/")
async def detect_expression(file: UploadFile = File(...)):
    try:
        # Read image
        contents = await file.read()
        image = np.array(Image.open(BytesIO(contents)).convert("RGB"))

        # Detect faces
        results = detector.detect_faces(image)
        
        if not results:
            return JSONResponse({"error": "No faces detected."})

        for result in results:
            x, y, width, height = result['box']
            x, y = max(0, x), max(0, y)  # Handle negative values

            # Crop the face
            face = image[y:y + height, x:x + width]

            # Preprocess the face
            face_gray = cv2.cvtColor(face, cv2.COLOR_RGB2GRAY)
            face_resized = cv2.resize(face_gray, (48, 48))
            face_normalized = face_resized / 255.0
            face_reshaped = np.reshape(face_normalized, (1, 48, 48, 1))

            # Predict expression
            predictions = model.predict(face_reshaped)
            emotion = emotion_labels[np.argmax(predictions)]

            # Draw bounding box and label
            cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)
            cv2.putText(image, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Convert image back to bytes
        _, buffer = cv2.imencode(".jpg", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        return StreamingResponse(BytesIO(buffer.tobytes()), media_type="image/jpeg")
    except Exception as e:
        return JSONResponse({"error": str(e)})

