import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = "Images Attendance"
images = []
classNames = []
myList = os.listdir(path)
#print(myList)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

#print(classNames)

def markAttendance(name):
    with open("Attendance.csv", "r+") as f:
        myDataLst = f.readlines()
        nameLst = []
        for line in myDataLst:
            entry = line.split(',')
            nameLst.append(entry[0])

        if name not in nameLst:
            now = datetime.now()
            dateStr = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name}, {dateStr}')

def findEncode(images):
    allEncode = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        allEncode.append(encode)

    return  allEncode

encodLstKnown = findEncode(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

    faceLocCurFr = face_recognition.face_locations(imgSmall)
    encodeCurFr = face_recognition.face_encodings(imgSmall, faceLocCurFr)

    for encodeFace, faceLoc in zip(encodeCurFr, faceLocCurFr):
        matches = face_recognition.compare_faces(encodLstKnown, encodeFace)
        faceDist = face_recognition.face_distance(encodLstKnown, encodeFace)
        #print(faceDist)
        matchIdx = np.argmin(faceDist)

        if matches[matchIdx]:
            name = classNames[matchIdx].upper()
            #print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
            markAttendance(name)

    cv2.imshow("Attendance Project", img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break