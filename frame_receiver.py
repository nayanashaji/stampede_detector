from flask import Flask, request
import cv2
import numpy as np
import datetime
from fluvio import Fluvio

# --- Flask Setup ---
app = Flask(__name__)

# --- Fluvio Setup ---
fluvio = Fluvio.connect()
producer = fluvio.topic_producer("crowd-topic")

@app.route('/frame', methods=['POST'])
def receive_frame():
    if 'image' not in request.files:
        return 'No image part', 400

    file = request.files['image']
    npimg = np.frombuffer(file.read(), np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # 👁️ Show the received frame in WSL
    cv2.imshow("Live Webcam (from Windows)", frame)
    cv2.waitKey(1)

    # 🧠 Stub logic for crowd analysis (replace with real logic)
    now = datetime.datetime.now()
    crowd_info = {
        "timestamp": now.isoformat(),
        "density": "low",  # Change this dynamically later
    }

    # 🚀 Send crowd info to Fluvio topic
    producer.send_string("crowd_key", str(crowd_info))

    print(f"[{now}] Frame received & pushed to Fluvio!")

    return 'Frame received', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
