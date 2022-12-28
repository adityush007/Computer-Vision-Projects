import cv2
import pickle
import face_recognition
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' : "https://real-time-attendance-56aee-default-rtdb.firebaseio.com/",
    'storageBucket' : "real-time-attendance-56aee.appspot.com"
})

#Importing Images of Students
SmodePath = "Images"
studentPath = os.listdir(SmodePath)

studentIds = []
imglst = []

for path in studentPath:
    imglst.append(cv2.imread(os.path.join(SmodePath, path)))
    studentIds.append(os.path.splitext(path)[0])

    fileName = f'{SmodePath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print(studentIds)

def findEncode(imglst):
    allEncode = []
    for img in imglst:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        allEncode.append(encode)

    return  allEncode

print("Encoding Started!...")
encodeLstKnown = findEncode(imglst)
encodeLstKnownwithIDs = [encodeLstKnown, studentIds]
print("Encoding Complete!")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeLstKnownwithIDs, file)
file.close()
print("File Saved!")