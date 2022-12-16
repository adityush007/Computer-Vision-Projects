import cv2
import numpy as np
import FMModule as fmm
import PTModule as ptm

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = fmm.FaceMeshDetector(max_num_faces=1)
plotY = ptm.LivePlot(640, 480, [25, 50], invert=True)

idlst = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
ratiolst = []
count = 0
frame = 0
color = (255, 0, 255)

while True:
    #If capturing a video on device
    # if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
    #       cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        for id in idlst:
            cv2.circle(img, face[id], 3, color, cv2.FILLED)

        leftUp = face[159]
        leftDown = face[23]
        leftlt = face[130]
        leftrt = face[243]

        verlength, _ = detector.findDistance(leftUp, leftDown)
        horlength, _ = detector.findDistance(leftlt, leftrt)

        cv2.line(img, leftUp, leftDown, (0, 255, 0), 2)
        cv2.line(img, leftlt, leftrt, (0, 255, 0), 2)

        ratio = int((verlength/horlength)*100)
        ratiolst.append(ratio)
        if len(ratiolst)>3:
            ratiolst.pop(0)

        avgRatio = sum(ratiolst)/len(ratiolst)

        if avgRatio < 37 and frame == 0:
            count += 1
            color = (0, 200, 0)
            frame = 1
        if frame != 0:
            frame += 1
            if frame > 10:
                frame = 0
                color = (255, 0, 255)

        cv2.rectangle(img, (0, 0), (225, 27), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, f'Blink Counter: {count}', (0, 20), cv2.FONT_HERSHEY_PLAIN, 1.5, color, 2)

        imgPlot = plotY.update(avgRatio, color)
        imgStack = np.hstack((img, imgPlot))
    else:
        imgStack = np.hstack((img, img))

    cv2.imshow("Blink Counter", imgStack)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break