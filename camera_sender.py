import cv2
import time
import os

# Change this path to a shared directory both Windows and WSL can access
save_path = "C:\\Users\\Nayana\\frame.jpg"

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Resize to a manageable size
    frame = cv2.resize(frame, (640, 480))

    # Save the frame
    cv2.imwrite(save_path, frame)
    print("Frame saved.")

    # Optional: show it on Windows too
    # cv2.imshow("Windows View", frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

    time.sleep(0.1)  # Adjust as needed

cap.release()
# cv2.destroyAllWindows()
