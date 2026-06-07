import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# Simulated Drone Data
altitude = 10.0
battery = 100.0

while True:

    ret, frame = cap.read()

    if not ret:
        break

    h, w = frame.shape[:2]

    center_x = w // 2
    center_y = h // 2

    # Camera center
    cv2.circle(frame, (center_x, center_y), 6, (0, 0, 255), -1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(
        gray,
        80,
        255,
        cv2.THRESH_BINARY_INV
    )

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    found = False

    battery -= 0.005

    if battery < 0:
        battery = 0

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area > 5000:

            x, y, width, height = cv2.boundingRect(cnt)

            ratio = width / float(height)

            # Detect square shape
            if 0.8 < ratio < 1.2:

                found = True

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + width, y + height),
                    (0, 255, 0),
                    3
                )

                marker_x = x + width // 2
                marker_y = y + height // 2

                cv2.circle(
                    frame,
                    (marker_x, marker_y),
                    6,
                    (255, 0, 0),
                    -1
                )

                error_x = marker_x - center_x
                error_y = marker_y - center_y

                # Decision Logic
                if error_x > 50:
                    action = "MOVE RIGHT"

                elif error_x < -50:
                    action = "MOVE LEFT"

                elif error_y > 50:
                    action = "MOVE BACKWARD"

                elif error_y < -50:
                    action = "MOVE FORWARD"

                else:
                    action = "AUTO LANDING INITIATED"

                    if altitude > 0:
                        altitude -= 0.1

                    if altitude < 0:
                        altitude = 0

                # Display Action
                cv2.putText(
                    frame,
                    action,
                    (40, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

                # Error Values
                cv2.putText(
                    frame,
                    f"X Error: {error_x}",
                    (40, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Y Error: {error_y}",
                    (40, 130),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 0),
                    2
                )

                break

    if not found:

        cv2.putText(
            frame,
            "SEARCHING LANDING PAD",
            (40, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

    # Altitude Display
    cv2.putText(
        frame,
        f"Altitude: {altitude:.1f} m",
        (40, 180),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    # Battery Display
    cv2.putText(
        frame,
        f"Battery: {battery:.0f}%",
        (40, 220),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    # Mission Success
    if altitude <= 0:

        cv2.putText(
            frame,
            "MISSION SUCCESS",
            (150, 300),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 255, 0),
            3
        )

    cv2.imshow(
        "AI Precision Landing System",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()