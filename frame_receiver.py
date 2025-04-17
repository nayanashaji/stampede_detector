from flask import Flask, request
import cv2
import numpy as np
import datetime

app = Flask(__name__)

@app.route('/frame', methods=['POST'])
def receive_frame():
    if 'image' not in request.files:
        return 'No image part', 400

    file = request.files['image']
    npimg = np.frombuffer(file.read(), np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # You can now pass this frame to your Fluvio processing pipeline
    print(f"[{datetime.datetime.now()}] Frame received!")

    # Optional: Show frame for testing
    # cv2.imshow("Received", frame)
    # cv2.waitKey(1)

    return 'Frame received', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
