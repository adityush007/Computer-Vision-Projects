import cv2
import FMModule as fmm
import FDModule as fdm
import numpy as np 

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
detector = fmm.FaceMeshDetector(max_num_faces=1)
detection = fdm.FaceDetector()

sen = 12

textList = ["Yahallo!", "Who's There?", "Its somebody", 
            "trying out", "things with", "OpenCV."]

while True:
    success, img = cap.read()
    imgText = np.zeros_like(img)
    img, faces = detector.findFaceMesh(img, draw=False)
    img, bbox = detection.findFaces(img, draw=True)

    if faces:
        face = faces[0]
        pointleft = face[145]
        pointright = face[374]

        W = 6.3
        d = 60
        w, _ = detector.findDistance(pointleft, pointright)

        #Finding Depth
        f = 700
        d = (W*f)/w
        #print(d)

        #Display
        scale = 2
        thickness = 3
        ox, oy = face[109][0]-90, face[109][1]-75
        (w, h), _ = cv2.getTextSize(f'Depth: {int(d)}cms', cv2.FONT_HERSHEY_PLAIN, scale, thickness)
        x1, y1, x2, y2 = ox - 10, oy + 10, ox + w + 10, oy - h - 10
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 255), cv2.FILLED)
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
        cv2.putText(img, f'Depth: {int(d)}cms', (ox, oy), cv2.FONT_HERSHEY_PLAIN, scale, (0, 0, 0), thickness)

        for i, text in enumerate(textList):
            singleheight = 20 + int((int(d/sen)*sen)/3)
            bscale = 0.4 + (int(d/sen)*sen)/85

            cv2.putText(imgText, text, (50, 50+(i*singleheight)), cv2.FONT_ITALIC,
                        bscale, (255, 255, 255), 2)
        
    imgStack = np.hstack((img, imgText))
    cv2.imshow("Video", imgStack)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()