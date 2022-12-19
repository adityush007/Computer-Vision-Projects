import cv2 
import HTModule as htm
import CVUtility as cvu
import time
import random

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = htm.handDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0, 0] #AI and Player Score respectively

while True:
    imgBG = cv2.imread("RPS/BG.png")
    success, img = cap.read()

    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80 : 480]

    hands, img = detector.findHands(imgScaled)

    if startGame:

        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 0), 4)

            if timer>3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingerCount(hand)

                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1
                    
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2

                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3
                    
                    randomNumber = random.randint(1, 3)
                    imgAI = cv2.imread(f"RPS/{randomNumber}.png", cv2.IMREAD_UNCHANGED)
                    imgBG = cvu.overlayPNG(imgBG, imgAI, (149, 310))

                    #When Player wins
                    if (playerMove == 1 and randomNumber == 3) or \
                        (playerMove == 2 and randomNumber == 1) or \
                        (playerMove == 3 and randomNumber == 2):
                        scores[1]+=1
                    
                    #When AI wins
                    if (playerMove == 3 and randomNumber == 1) or \
                        (playerMove == 1 and randomNumber == 2) or \
                        (playerMove == 2 and randomNumber == 3):
                        scores[0]+=1

                    print(playerMove)

    imgBG[234:654, 795:1195] = imgScaled

    if stateResult:
        imgBG = cvu.overlayPNG(imgBG, imgAI, (149, 310))

    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    
    cv2.imshow("Rock Paper Scissor Game", imgBG)
    key =  cv2.waitKey(1)

    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False

    elif key == ord('q'):
        break
