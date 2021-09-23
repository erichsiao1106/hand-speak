import cv2
import mediapipe as mp
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands = 2,min_detection_confidence=0.8, min_tracking_confidence=0.8)
drawing_spec = mp_drawing.DrawingSpec(color=(255, 255, 255),thickness=8, circle_radius=8)

tipIds = [4, 8, 12, 16, 20]
cap = cv2.VideoCapture(0)
while cap.isOpened():
    prev_time = time.time()
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    lmList = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks,mp_hands.HAND_CONNECTIONS,drawing_spec,drawing_spec)

            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                # print(lmList)
                cv2.circle(frame, (cx, cy), 8, (38, 107, 170), cv2.FILLED)
                if id == 3 or id == 4 or id == 8 or id == 12 or id == 16 or id == 20:
                    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), cv2.FILLED)
                    cv2.putText(frame,str(id),(cx+8, cy),cv2.FONT_HERSHEY_COMPLEX,.6,(0,0,255),1)
            if len(lmList) != 0:
                fingers = []
                # Thumb
                if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                    print(lmList[tipIds[0]][1], lmList[tipIds[0] - 1][1])
                    fingers.append(1)
                else:
                    fingers.append(0)
                # 4 Fingers
                for id in range(1, 5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                totalFingers = fingers.count(1)
                print(totalFingers)
    else:
        totalFingers = 0

    cv2.rectangle(frame, (6, 121), (114, 229), (255, 255, 255), cv2.FILLED)
    cv2.rectangle(frame, (10, 125), (110, 225), (0, 0, 0), cv2.FILLED)
    if totalFingers==5:
        cv2.putText(frame, str(totalFingers), (30, 210), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 0), 8)
    else:
        cv2.putText(frame, str(totalFingers), (30, 210), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 255), 8)
    cv2.putText(frame, 'fps:'+str(int(1 / (time.time() - prev_time))), (3, 40), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
    print(1 / (time.time() - prev_time))
    cv2.imshow('finger counter', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()