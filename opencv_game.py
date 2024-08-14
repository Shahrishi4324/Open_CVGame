import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import random

# Initialize webcam
cap = cv2.VideoCapture(0)

# Initialize hand detector
detector = HandDetector(maxHands=1, detectionCon=0.8)

# Player object properties
x, y = 400, 300
radius = 30

# Obstacles
obstacles = [
    {'x': 100, 'y': 150, 'size': 40},
    {'x': 500, 'y': 350, 'size': 40},
    {'x': 300, 'y': 250, 'size': 40},
]

# Power-ups
power_ups = [
    {'x': random.randint(50, 600), 'y': random.randint(50, 400), 'size': 20, 'type': 'invincibility'},
    {'x': random.randint(50, 600), 'y': random.randint(50, 400), 'size': 20, 'type': 'double_points'}
]

# Game settings
score = 0
lives = 3
invincible = False
double_points = False
invincibility_timer = 0
double_points_timer = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)

        # Move the player based on hand gestures
        if fingers == [0, 0, 0, 0, 0]:
            y += 20  # Move down
        elif fingers == [1, 1, 1, 1, 1]:
            y -= 20  # Move up
        elif fingers == [0, 1, 0, 0, 0]:
            x += 20  # Move right
        elif fingers == [1, 0, 0, 0, 0]:
            x -= 20  # Move left

        # Ensure player stays within screen bounds
        x = max(radius, min(x, 640 - radius))
        y = max(radius, min(y, 480 - radius))

    # Handle obstacle collisions
    remaining_obstacles = []
    for obstacle in obstacles:
        ox, oy = obstacle['x'], obstacle['y']
        size = obstacle['size']
        cv2.rectangle(img, (ox, oy), (ox + size, oy + size), (0, 255, 0), -1)

        # Check for collision with obstacle
        if (ox < x < ox + size) and (oy < y < oy + size):
            if not invincible:
                lives -= 1
                if lives == 0:
                    cv2.putText(img, "Game Over", (220, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                    cv2.imshow("Hand Gesture Game", img)
                    cv2.waitKey(3000)
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()
        else:
            remaining_obstacles.append(obstacle)

    obstacles = remaining_obstacles

    # Handle power-ups collection
    remaining_power_ups = []
    for power_up in power_ups:
        px, py = power_up['x'], power_up['y']
        size = power_up['size']
        power_type = power_up['type']

        # Display power-up on the screen
        color = (255, 255, 0) if power_type == 'invincibility' else (255, 0, 255)
        cv2.circle(img, (px, py), size, color, -1)

        # Check for collision with power-up
        if (px - size < x < px + size) and (py - size < y < py + size):
            if power_type == 'invincibility':
                invincible = True
                invincibility_timer = 200
            elif power_type == 'double_points':
                double_points = True
                double_points_timer = 200
        else:
            remaining_power_ups.append(power_up)

    power_ups = remaining_power_ups

    # Update score and manage power-up timers
    if double_points:
        score += 2
        double_points_timer -= 1
        if double_points_timer <= 0:
            double_points = False
    else:
        score += 1

    if invincible:
        invincibility_timer -= 1
        if invincibility_timer <= 0:
            invincible = False

    # Draw player and display game information
    cv2.circle(img, (x, y), radius, (255, 0, 0), -1)
    cv2.putText(img, f"Score: {score}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(img, f"Lives: {lives}", (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Show the game window
    cv2.imshow("Hand Gesture Game with Power-Ups", img)

    # Exit the game on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
