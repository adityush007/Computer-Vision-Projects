import cv2
import mediapipe as mp
import time

class FaceMeshDetector():

    def __init__(self,
                static_image_mode=False,
                max_num_faces=2,
                refine_landmarks=False,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5):

        self.static_image_mode = static_image_mode
        self.max_num_faces = max_num_faces
        self.refine_landmarks = refine_landmarks
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.static_image_mode,
                                                self.max_num_faces,
                                                self.refine_landmarks,
                                                self.min_detection_confidence,
                                                self.min_tracking_confidence)
        self.drawSpec = self.mpDraw.DrawingSpec(color= (0, 255, 0), thickness=1, circle_radius=1)

    def findFaceMesh(self, img, draw = True):
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(self.imgRGB)

        faces = []
        if self.results.multi_face_landmarks:
            for faceLm in self.results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, faceLm, self.mpFaceMesh.FACEMESH_CONTOURS,
                                        self.drawSpec, self.drawSpec)
                face = []
                for id, lm in enumerate(faceLm.landmark):
                    #print(lm)
                    ih, iw, ic = img.shape
                    x, y = int(lm.x*iw), int(lm.y*ih)
                    #print(id, x, y)
                    face.append([x, y])
                faces.append(face)

        return img, faces

def main():
    cTime, pTime = 0, 0
    cap = cv2.VideoCapture(0)

    detector = FaceMeshDetector()

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img, faces = detector.findFaceMesh(img)

        if len(faces) != 0:
            print(len(faces))

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS : {int(fps)}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)

        cv2.imshow("Video", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()
