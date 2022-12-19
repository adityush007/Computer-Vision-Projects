import cv2
import mediapipe as mp 
import time

class poseDetector:
    def __init__ (self, static_image_mode = False, model_complexity = 1, smooth_landmarks = True, enable_segmentation = False, smooth_segmentation = True, min_detection_confidence = 0.5, min_tracking_confidence = 0.5):

        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.static_image_mode, self.model_complexity, self.smooth_landmarks, self.enable_segmentation,
                                     self.smooth_segmentation, self.min_detection_confidence, self.min_tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils
        self.lmlist = []

    def findPose(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img

    def findPositions(self, img, draw = True):
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                #print(id, lm)
                cx, cy = int(lm.x*w), int(lm.y*h)
                self.lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx,cy), 5, (255, 0, 0), cv2.FILLED)

        return self.lmlist

def main():
    pTime = 0
    detector = poseDetector()
    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmlist = detector.findPositions(img)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, f'FPS : {int(fps)}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)

        cv2.imshow("Video", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()