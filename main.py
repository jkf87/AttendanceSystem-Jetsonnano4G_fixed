import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pytz
import csv

def identifyEncodings(images):
    encodeList = []
    for img in images:
        try:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except Exception as e:
            print(f"Error encoding image: {e}")
    return encodeList

def markAttendance(name):
    date = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%y_%m_%d")
    file_path = f'Attendance_Entry/Attendance_{date}.csv'
    
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(header)

    try:
        with open(file_path, 'r+') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
            
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                date_i = now.strftime('%Y-%m-%d')
                f.writelines(f'\n{name},{dtString},{date_i}')
    except Exception as e:
        print(f"Error marking attendance: {e}")


if not os.path.exists('Attendance_Entry'):
    os.makedirs('Attendance_Entry')

date = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%y_%m_%d")
header = ("S.NO", "Time", "Date")

try:
    if not os.path.exists(f"Attendance_Entry/Attendance_{date}.csv"):
        with open(f"Attendance_Entry/Attendance_{date}.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(header)
except Exception as e:
    print(f"Error creating initial CSV: {e}")

try:
    path = 'Attendance_data'
    images = []
    classNames = []
    myList = os.listdir(path)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    encodeListKnown = identifyEncodings(images)
    del images
    print('Encoding Complete')
except Exception as e:
    print(f"Error during preprocessing: {e}")

try:
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        exit()
    
    while True:
        success, img = cap.read()
        if not success or img is None:
            print("Error: Failed to read frame from video stream.")
            continue

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
except Exception as e:
    print(f"Error during face recognition: {e}")
finally:
    cap.release()
    cv2.destroyAllWindows()
