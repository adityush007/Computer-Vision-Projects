import cv2
import mediapipe as mp 
import time

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

cTime, pTime = 0, 0
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            print(id, lm)
            cx, cy = int(lm.x*w), int(lm.y*h)
            cv2.circle(img, (cx,cy), 5, (255, 0, 0), cv2.FILLED)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS : {int(fps)}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)

    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break