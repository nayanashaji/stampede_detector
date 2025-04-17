import cv2
import requests
import time

# Change this if your WSL IP is different
WSL_SERVER_URL = 'http://localhost:5000/frame'

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Resize to reduce data size if needed
    frame = cv2.resize(frame, (640, 480))

    # Encode frame as JPEG
    _, img_encoded = cv2.imencode('.jpg', frame)
    response = requests.post(WSL_SERVER_URL, files={'image': img_encoded.tobytes()})

    print(f"Status: {response.status_code}")
    time.sleep(0.1)  # optional: reduce spam

cap.release()
