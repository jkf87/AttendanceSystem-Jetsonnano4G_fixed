
import cv2
import numpy as np
import face_recognition
import os
import gc
import time
from datetime import datetime
from datetime import date
import pytz
import csv

def identifyEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except Exception as e:
            print(f"Error encoding image: {e}")
    return encodeList

def markAttendance(name):
    date = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%y_%m_%d||%H:%M")
    try:
        with open(f'Attendance_Entry/Attendance_{date}.csv', 'r+') as f:
            myDataList = f.readlines()
            nameList = [line.split(',')[0] for line in myDataList]
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                date_i = now.strftime('%Y-%m-%d')
                f.writelines(f'
{name},{dtString},{date_i}')
    except Exception as e:
        print(f"Error marking attendance: {e}")

date = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%y_%m_%d||%H:%M")
header = ("S.NO","Time","Date")

try:
    with open(f"Attendance_Entry/Attendance_{date}.csv","w") as file:
        writer = csv.writer(file)
        writer.writerow(header)
except Exception as e:
    print(f"Error creating attendance file: {e}")

path = 'Attendance_data'
images = []
classNames = []
myList = os.listdir(path)
for cl in myList:
    try:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    except Exception as e:
        print(f"Error reading image: {e}")

encodeListKnown = identifyEncodings(images)
gc.collect()
print('Encoding Complete')

cap = cv2.VideoCapture('/dev/video0')
start_time = time.time()

while True:
    try:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markAttendance(name)

        cv2.imshow('Attendance System', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if time.time() - start_time > 3600:
            encodeListKnown = []
            start_time = time.time()

    except Exception as e:
        print(f"Error in main loop: {e}")

cap.release()
cv2.destroyAllWindows()
