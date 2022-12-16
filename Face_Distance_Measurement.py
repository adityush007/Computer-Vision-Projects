import cv2
import FMModule as fmm
import FDModule as fdm

cap = cv2.VideoCapture(0)
detector = fmm.FaceMeshDetector(max_num_faces=1)
detection = fdm.FaceDetector()

while True:
    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False)
    img, bbox = detection.findFaces(img, draw=True)

    if faces:
        face = faces[0]
        pointleft = face[145]
        pointright = face[374]
        
        #Drawing
        # cv2.line(img, pointleft, pointright, (0, 255, 0), 2)
        # cv2.circle(img, pointleft, 5, (255, 100, 200), cv2.FILLED)
        # cv2.circle(img, pointright, 5, (255, 100, 200), cv2.FILLED)

        W = 6.3
        d = 60
        w, _ = detector.findDistance(pointleft, pointright)

        #Parameters for finding Focal Length of the Web-Cam
        # f = (w*d)/W
        # print(f)

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

    cv2.imshow("Video", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()