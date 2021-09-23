import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands = 3, min_detection_confidence=0.5, min_tracking_confidence=0.5)
drawing_spec1 = mp_drawing.DrawingSpec(color=(255, 255, 255),thickness=8, circle_radius=8)

cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, c = image.shape
    results = hands.process(image)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            print(hand_landmarks)
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
            ,landmark_drawing_spec=drawing_spec1, connection_drawing_spec=drawing_spec1)
            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (cx, cy), 8, (255, 255, 0), cv2.FILLED)
                # 我比影片中多加了以下三行，猜猜看作用是什麼？
                if id == 8:
                    cv2.circle(frame, (cx, cy-15), 25, (0, 255, 0), cv2.FILLED)
                cv2.putText(frame,str(id),(cx+8, cy),cv2.FONT_HERSHEY_COMPLEX,.6,(0,0,255),1)
    cv2.imshow('hand002', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()