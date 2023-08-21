import cv2
import mediapipe as mp
import os

# инициализируем переменные для определения положения точек на руке
x1 = 0
y1 = 0
x2 = 0
y2 = 0

# инициализируем камеру OpenCV
webcamera = cv2.VideoCapture(0)
webcamera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
webcamera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
webcamera.set(cv2.CAP_PROP_FPS, 30)

my_hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.5)
drawing_utils = mp.solutions.drawing_utils

while True:
    _ , image = webcamera.read()
    image = cv2.flip(image,1)
    frame_heigth, frame_width, _ = image.shape
    rgb_image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks
    if hands :
        for hand in hands:
            drawing_utils.draw_landmarks(image,hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_heigth)
                if id == 8:
                    cv2.circle(img=image,center=(x,y), radius=8, color=(0, 255, 255), thickness=3)
                    x1 = x
                    y1 = y 
                if id == 4:
                    cv2.circle(img=image, center=(x,y), radius=4, color=(0, 0, 255), thickness=3)
                    x2 = x
                    y2 = y 
        dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        cv2.line(image,(x1, y1),(x2, y2),(0, 255, 0), 3)
        if dist >= 120 and dist < 160:
            command = "osascript -e 'set volume output volume 20'"
            os.system(command)
        elif dist >= 160 and dist < 200:
            command = "osascript -e 'set volume output volume 40'"
            os.system(command)
        elif dist >= 200 and dist < 240:
            command = "osascript -e 'set volume output volume 60'"
            os.system(command)
        elif dist >= 240 and dist < 280:
            command = "osascript -e 'set volume output volume 80'"
            os.system(command)
        elif dist >= 280 and dist < 320:
            command = "osascript -e 'set volume output volume 100'"
            os.system(command)
        else:
            command = "osascript -e 'set volume output volume (output volume of (get volume settings)) - 3'"
            os.system(command)
    cv2.imshow('Hand volume control', image)
    key = cv2.waitKey(10)
    if key == 27:
        break

webcamera.release()
cv2.destroyAllWindows()