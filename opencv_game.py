import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector

# Initialize webcam
cap = cv2.VideoCapture(0)

# Initialize hand detector
detector = HandDetector(maxHands=1, detectionCon=0.8)

# Object properties
x, y = 400, 300
radius = 30

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)

        if fingers == [0, 0, 0, 0, 0]:
            y += 20  # Move down
        elif fingers == [1, 1, 1, 1, 1]:
            y -= 20  # Move up
        elif fingers == [0, 1, 0, 0, 0]:
            x += 20  # Move right
        elif fingers == [1, 0, 0, 0, 0]:
            x -= 20  # Move left

        # Boundary conditions
        if x < radius:
            x = radius
        if x > 640 - radius:
            x = 640 - radius
        if y < radius:
            y = radius
        if y > 480 - radius:
            y = 480 - radius

    # Draw the object
    cv2.circle(img, (x, y), radius, (255, 0, 0), -1)

    cv2.imshow("Hand Gesture Object Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()