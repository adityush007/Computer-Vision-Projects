import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
plateCascade = cv2.CascadeClassifier("Resources/haarcascades/haarcascade_russian_plate_number.xml")
min_area = 500
color = (0, 255, 0)

while True:
    success, img = cap.read()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    numbers = plateCascade.detectMultiScale(img_gray, 1.1, 4)

    for(x, y, w, h) in numbers:
        area = w*h
        if area>min_area:
            cv2.rectangle(img, (x, y), (x+w, h+y), (0, 255, 0), 2)
            cv2.putText(img, "Number Plate", (x,y-5), cv2.FONT_ITALIC, 1, color, 2)
            imgR = img[y:y+h, x:x+w]
            cv2.imshow("ROI", imgR)

    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break