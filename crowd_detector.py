from fluvio import Fluvio
import cv2
import numpy as np
import time

fluvio = Fluvio.connect()
producer = fluvio.topic_producer("crowd-density")


# Load the MobileNet SSD model
net = cv2.dnn.readNetFromCaffe("models/MobileNetSSD_deploy.prototxt",
                               "models/MobileNetSSD_deploy.caffemodel")

# Load the COCO class labels
with open("models/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Prepare the frame for prediction
    h, w = frame.shape[:2]
    net.setInput(cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5, 127.5, 127.5, False))

    # Perform forward pass
    detections = net.forward()

    # Loop over the detections and draw bounding boxes for the detected objects
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        # Only consider detections with a confidence greater than 0.2
        if confidence > 0.2:
            class_id = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x1, y1, x2, y2) = box.astype("int")

            # Draw the bounding box
            label = "{}: {:.2f}".format(classes[class_id], confidence)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            y = y1 - 10 if y1 - 10 > 10 else y1 + 10
            cv2.putText(frame, label, (x1, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the frame with bounding boxes
    cv2.imshow("Crowd Detector", frame)

    # Send data to Fluvio
    producer.send(bytes(str(detections), 'utf-8'))

    # Wait for the key press to quit the video feed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup and close everything
cap.release()
cv2.destroyAllWindows()
