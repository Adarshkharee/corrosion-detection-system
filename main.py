import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define red color range in HSV
    lower_red1 = np.array([0, 70, 70])
    upper_red1 = np.array([20, 200, 150])

    lower_red2 = np.array([170, 70, 70])
    upper_red2 = np.array([180, 200, 150])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    full_mask = mask1 + mask2

    corrosion_pixels = cv2.countNonZero(full_mask)
    total_pixels = frame.shape[0] * frame.shape[1]
    corrosion_percent = (corrosion_pixels / total_pixels) * 100

    output = cv2.bitwise_and(frame, frame, mask=full_mask)

    cv2.putText(frame, f'Corrosion: {corrosion_percent:.2f}%', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow('Original', frame)
    cv2.imshow('Detected Corrosion', output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()