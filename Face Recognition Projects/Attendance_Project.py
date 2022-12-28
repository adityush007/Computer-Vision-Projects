import cv2
import os
import pickle
import face_recognition
import CVUtility as cvu
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
from threading import Thread

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' : "https://real-time-attendance-56aee-default-rtdb.firebaseio.com/",
    'storageBucket' : "real-time-attendance-56aee.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)

# Importing images of different modes in a list

imgBg = cv2.imread("Resources/background.png")
FmodePath = "Resources/Modes"
modePath = os.listdir(FmodePath)

imgModelst = []
for path in modePath:
    imgModelst.append(cv2.imread(os.path.join(FmodePath, path)))

# print(len(imgModelst))

#Loading Encodings File

print("Loading Encoding File!..")
file = open("EncodeFile.p", 'rb')
encodeLstKnownwithIDs = pickle.load(file)
file.close()
encodeLstKnown, studentIds = encodeLstKnownwithIDs
# print(studentIds)
print("Encode File Loaded!")

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()
    imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

    faceLocCurFr = face_recognition.face_locations(imgSmall)
    encodeCurFr = face_recognition.face_encodings(imgSmall, faceLocCurFr)

    imgBg[162 : 162+480, 55 : 55+640] = img
    imgBg[44 : 44+633, 808 : 808+414] = imgModelst[modeType]

    if faceLocCurFr:
        for encodeFace, faceLoc in zip(encodeCurFr, faceLocCurFr):
            matches = face_recognition.compare_faces(encodeLstKnown, encodeFace, tolerance=0.5)
            faceDist = face_recognition.face_distance(encodeLstKnown, encodeFace)
            # print("FaceDist", faceDist)
            # print("Matches", matches)

            matchIdx = np.argmin(faceDist)
            # print("Match Index", matchIdx)

            if matches[matchIdx]:
                # print("Know Face Detected", studentIds[matchIdx])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                bbox = 55 + x1, 162 + y1, x2-x1, y2-y1
                #print(bbox)
                imgBg =  cvu.cornerRect(imgBg, bbox, rt=0)
                id = studentIds[matchIdx]
                if counter == 0:
                    cvu.putTextRect(imgBg, "Loading..", (275, 400))
                    cv2.imshow("Attendance Window", imgBg)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:
            if counter == 1:
                #Getting Data from DataBase
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)

                #Getting Images from Storage
                blob = bucket.get_blob(f'Images/{id}.jpg')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                #Updating Data of Attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendace_time'],
                                "%Y-%m-%d %H:%M:%S")
                secondElapsed = (datetime.now()-datetimeObject).total_seconds()
                print(secondElapsed)

                if secondElapsed > 30:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] +=1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendace_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                else:
                    modeType = 3
                    counter = 0
                    imgBg[44 : 44+633, 808 : 808+414] = imgModelst[modeType]

            if modeType != 3:
            
                if 10<counter<20:
                    modeType = 2
                    imgBg[44 : 44+633, 808 : 808+414] = imgModelst[modeType]

                if counter <= 10:
                    cv2.putText(imgBg, str(studentInfo['total_attendance']),
                                (861, 125), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBg, str(studentInfo['major']),
                                (1006, 550), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBg, str(id),
                                (1006, 493), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBg, str(studentInfo['Grade']),
                                (910, 625), cv2.FONT_HERSHEY_DUPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBg, str(studentInfo['year']),
                                (1025, 625), cv2.FONT_HERSHEY_DUPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBg, str(studentInfo['starting_year']),
                                (1125, 625), cv2.FONT_HERSHEY_DUPLEX, 0.6, (100, 100, 100), 1)

                    (w, h), _ = cv2.getTextSize(str(studentInfo['name']), cv2.FONT_HERSHEY_DUPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBg, str(studentInfo['name']),
                                (808 + offset, 445), cv2.FONT_HERSHEY_DUPLEX, 1, (50, 50, 50), 1)

                    imgBg[175: 175+216, 909: 909+216] = imgStudent

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBg[44 : 44 + 633, 808 : 808 + 414] = imgModelst[modeType]

    else:
        modeType = 0
        counter = 0
    
    cv2.imshow("Attendance Window", imgBg)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break