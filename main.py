import cv2
import mediapipe as mp
import pyautogui
import pyttsx3
import time
import math
from collections import deque

# Initialize voice
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Screen size
screen_w, screen_h = pyautogui.size()

# Cursor smoothing
prev_x, prev_y = 0, 0
smoothing = 8

# Gesture tracking
gesture_history = deque(maxlen=5)  # Store last 5 frames
click_cooldown = 0.7
last_click_time = 0

lock_state = False
last_lock_time = 0
lock_cooldown = 1

# Helper functions
def fingers_up(hand_landmarks):
    fingers = []
    tip_ids = [4, 8, 12, 16, 20]

    # Thumb
    if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other 4 fingers
    for id in range(1, 5):
        if hand_landmarks.landmark[tip_ids[id]].y < hand_landmarks.landmark[tip_ids[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

def distance(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

def is_consistent_gesture(expected_total):
    # Count how many times expected gesture appeared in last frames
    return gesture_history.count(expected_total) >= 3

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_img)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm_list = hand_landmarks.landmark
            fingers = fingers_up(hand_landmarks)
            total_fingers = fingers.count(1)
            gesture_history.append(total_fingers)

            # Coordinates
            x1, y1 = lm_list[8].x, lm_list[8].y
            screen_x = screen_w * x1
            screen_y = screen_h * y1

            curr_x = prev_x + (screen_x - prev_x) / smoothing
            curr_y = prev_y + (screen_y - prev_y) / smoothing

            # --- Move Mouse ---
            if not lock_state and fingers[1] == 1 and total_fingers == 1:
                pyautogui.moveTo(curr_x, curr_y)

            prev_x, prev_y = curr_x, curr_y

            # --- Left Click: Thumb + Index close ---
            if fingers[0] == 1 and fingers[1] == 1 and total_fingers == 2:
                dist = distance(lm_list[4], lm_list[8])
                if dist < 0.06 and is_consistent_gesture(2):
                    if time.time() - last_click_time > click_cooldown:
                        pyautogui.click()
                        speak("Click")
                        last_click_time = time.time()

            # --- Right Click: Index + Middle close ---
            if fingers[1] == 1 and fingers[2] == 1 and total_fingers == 2:
                dist = distance(lm_list[8], lm_list[12])
                if dist < 0.035 and is_consistent_gesture(2):
                    if time.time() - last_click_time > click_cooldown:
                        pyautogui.rightClick()
                        speak("Right Click")
                        last_click_time = time.time()

            # --- Scroll with 3 fingers ---
            if total_fingers == 3 and is_consistent_gesture(3):
                if lm_list[8].y < lm_list[12].y:
                    pyautogui.scroll(50)
                else:
                    pyautogui.scroll(-50)

            # Draw hand landmarks
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Draw cursor following hand
            cursor_x = int(x1 * 640)
            cursor_y = int(y1 * 480)
            cv2.circle(img, (cursor_x, cursor_y), 10, (255, 255, 0), cv2.FILLED)

    # ===============================
    # Show Gesture Status on Screen
    # ===============================
    # Click Readiness Status
    click_text = "Ready" if time.time() - last_click_time > click_cooldown else "Cooldown"
    click_color = (0, 255, 0) if click_text == "Ready" else (0, 0, 255)
    cv2.putText(img, f"Click: {click_text}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX,
                1, click_color, 2)

    # Show webcam feed
    cv2.imshow("Virtual Mouse", img)

    if cv2.waitKey(1) == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
