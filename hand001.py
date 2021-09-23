import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands = 3, min_detection_confidence=0.5, min_tracking_confidence=0.5)
drawing_spec1 = mp_drawing.DrawingSpec(color=(255, 255, 255),thickness=8, circle_radius=8)
drawing_spec2 = mp_drawing.DrawingSpec(color=(255, 255, 0),thickness=8, circle_radius=8)

cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
            ,landmark_drawing_spec=drawing_spec2, connection_drawing_spec=drawing_spec1)
    cv2.imshow('hand001', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()