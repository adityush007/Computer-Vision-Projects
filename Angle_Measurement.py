import math
import cv2

pointslst = []

path = "Resources/acute-angles.png"
img = cv2.imread(path)

def mousePoints(event,x,y,flags,params):
    if event == cv2.EVENT_LBUTTONDOWN:
        size = len(pointslst)
        if size != 0 and size % 3 != 0:
            cv2.line(img,tuple(pointslst[round((size-1)/3)*3]), (x,y), (0,0,255), 2)
        cv2.circle(img, (x,y), 5, (0,0,255), cv2.FILLED)
        pointslst.append([x,y])

def gradient(pt1, pt2):
    return ((pt2[1]-pt1[1])/(pt2[0]-pt1[0]))

def getAngle(pointslst):
    pt1, pt2, pt3 = pointslst[-3:]
    m1 = gradient(pt1, pt2)
    m2 = gradient(pt1, pt3)
    angR = math.atan((m2-m1)/(1+(m2*m1)))
    angD = round(math.degrees(angR))
    cv2.putText(img, str(angD), (pt1[0]-40, pt1[1]-20), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)

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
