import cv2
import random
import numpy as np
import HTModule as htm
import time
import math

cap = cv2.VideoCapture(0)

cTime, pTime = 0, 0

detector = htm.handDetector(maxHands=1, detectionCon=0.8)

#Find Function
#X is the raw distance, y is the value in cms
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]

coeff = np.polyfit(x, y, 2)     # Coeff. of quadratic equation

#Game Variables
cx, cy = 150, 250     #Intial Value of Game Button
color = (13, 113, 219)
counter = 0
score = 0
timeStart = time.time()
totalTime = 32

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    if time.time()-timeStart < totalTime:
        hands = detector.findHands(img, draw=False, flipType=False)

        if hands:
            lmlist = detector.findPosition(img, draw = False)
            x, y, w, h = hands[0]['bbox']
            #print(lmlist)
            if len(lmlist) != 0:
                x1, y1 = lmlist[5][1:]
                x2, y2 = lmlist[17][1:]

                distance = int(math.sqrt((y2-y1)**2 + (x2-x1)**2))
                A, B, C = coeff
                distCM = A*distance**2+ B*distance + C

                #print(distCM, distance)
                cv2.putText(img, f'Distance : {int(distCM)} cms', (x+80, y-25), cv2.FONT_HERSHEY_PLAIN, 1.3, (50, 100, 255), 2)
                
                if distCM < 40:
                    if x<cx<x+w and y<cy<y+h:
                        counter = 1
        
        if counter:
            counter+=1
            color = (0, 255, 0)
            if counter == 4:
                color = (13, 113, 219)
                cx = random.randint(100, 600)
                cy = random.randint(100, 450)
                score+=1
                counter = 0

        cv2.namedWindow("Game", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Game", 1080, 720)

        #Button
        cv2.circle(img, (cx, cy), 20, color, cv2.FILLED)
        cv2.circle(img, (cx, cy), 6, (255, 255, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 12, (255, 255, 255), 1)
        cv2.circle(img, (cx, cy), 20, (50, 50, 50), 2)

        # Game Display
        cv2.rectangle(img, (500, 27), (900, 0), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, f'Time: {int(totalTime-(time.time()-timeStart))}', (520, 20), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
        cv2.rectangle(img, (0, 0), (125, 27), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, f'Score: {str(score).zfill(2)}', (0, 20), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)

    else:
        cv2.rectangle(img, (390, 225), (240, 260), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, f'Game Over', (250, 250), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)

        cv2.rectangle(img, (375, 305), (250, 280), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, f'Score: {str(score).zfill(2)}', (260, 300), cv2.FONT_HERSHEY_PLAIN, 1.3, (255, 255, 255), 2)

        cv2.rectangle(img, (110, 355), (515, 330), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, "Press 'r' to Restart and 'q' to Quit", (120, 350), cv2.FONT_HERSHEY_PLAIN, 1.3, (255, 255, 255), 2)
    
    cv2.imshow("Game", img)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break
    elif key == ord('r'):
        timeStart = time.time()
        score = 0

cap.release()
cv2.destroyAllWindows()
