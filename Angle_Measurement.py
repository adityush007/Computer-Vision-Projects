import math
import cv2

pointslst = []

path = "Resources/acute-angles.png"
img = cv2.imread(path)

def mousePoints (event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 5, (0, 0, 255), cv2.FILLED)
        pointslst.append([x, y])
        print(pointslst)
        #print(x, y)

def gradient(pt1, pt2):
    return ((pt2[1]-pt1[1])/(pt2[0]-pt1[0]))

def getAngle(pointslst):
    pt1, pt2, pt3 = pointslst[-3:]
    m1 = gradient(pt1, pt2)
    m2 = gradient(pt1, pt3)
    angR = math.atan((m2-m1)/(1+(m2*m1)))
    angD = round(math.degrees(angR))
    print(angD)

while True:
    if len(pointslst) % 3 == 0 and len(pointslst) != 0:
        getAngle(pointslst)

    cv2.imshow("Angles",img)
    cv2.setMouseCallback("Angles", mousePoints)
    if cv2.waitKey(1) & 0xFF == ord('r'):
        pointslst = []
        img = cv2.imread(path)
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        break