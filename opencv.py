import cv2
import mediapipe as mp
import random
video = cv2.VideoCapture(1)

picture = cv2.imread("papka/knb.jpg")

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
p = [0 for i in range(21)]
finger = [0 for i in range(5)]

img_knb = [0 for i in range(3)]
img_knb[0] = picture[0:150, 134:200] #камень
img_knb[1] = picture[0:150, 67:133] #ножницы
img_knb[2] = picture[0:150, 0:66] #бумага

def distance(point1, point2):
    return abs(point1-point2)

def knb(my_knb):
    img[0:150, 0:66] = img_knb[my_knb]
    rand_knb = random.randint(0, 2)
    img[0:150, 450:516] = img_knb[rand_knb]

    if rand_knb == my_knb:
        print("Ничья")
        cv2.putText(img, "Ничья", (200, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (200, 0, 0), 2)
    else:
        if rand_knb == 0:
            if my_knb == 1:
                print("Проигрыш")
                cv2.putText(img, "Проигрыш", (200, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 200), 2)
            else:
                print("Победа")
                cv2.putText(img, "Победа", (200, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 200, 0), 2)
        if rand_knb == 1:
            if my_knb == 0:
                print("Победа")
                cv2.putText(img, "Победа", (200, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 200, 0), 2)
            else:
                print("Проигрыш")
                cv2.putText(img, "Проигрыш", (200, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 200), 2)
        if rand_knb == 2:
            if my_knb == 1:
                print("Победа")
                cv2.putText(img, "Победа", (200, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 200, 0), 2)
            else:
                print("Проигрыш")
                cv2.putText(img, "Проигрыш", (200, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 200), 2)


while True:
    good, img = video.read()
    cameraRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(cameraRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            for id, point in enumerate(handLms.landmark):
                width, height, color = img.shape
                width, height = int(point.x * height), int(point.y * width)
                p[id] = height

        distanceGood = distance(p[0], p[5]) + distance(p[0], p[5])/2

        finger[1] = 1 if distance(p[0], p[8]) > distanceGood else 0
        finger[2] = 1 if distance(p[0], p[12]) > distanceGood else 0
        finger[3] = 1 if distance(p[0], p[16]) > distanceGood else 0
        finger[4] = 1 if distance(p[0], p[20]) > distanceGood else 0
        finger[0] = 1 if distance(p[4], p[17]) > distanceGood else 0

        if cv2.waitKey(1) == ord('s'):
            if not(finger[0]) and not(finger[1]) and not(finger[2]) and not(finger[3]) and not(finger[4]):
                print('Камень')
                knb(0)
            if not(finger[0]) and (finger[1]) and (finger[2]) and not(finger[3]) and not(finger[4]):
                print('Ножницы')
                knb(1)
            if not(finger[0]) and (finger[1]) and (finger[2]) and (finger[3]) and (finger[4]):
                print('Бумага')
                knb(2)
            cv2.imshow("Video", img)
            cv2.waitKey(3000)

    cv2.imshow("Video", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

