import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pytz
import csv

# 이미지 인코딩 함수 (Function to encode images)
def identifyEncodings(images):
    encodeList = []
    for img in images:
        try:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except Exception as e:
            print(f"이미지 인코딩 오류 (Error encoding image): {e}")
    return encodeList

# 출석 기록 함수 (Function to mark attendance)
def markAttendance(name):
    # 파일 이름에는 날짜만 포함 (Only include date in filename)
    date = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%y_%m_%d")
    file_path = f'Attendance_Entry/Attendance_{date}.csv'
    
    # Check if file exists
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
            
            # 이미 출석한 경우 추가 출석을 하지 않음 (If already attended, do not add again)
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                date_i = now.strftime('%Y-%m-%d')
                f.writelines(f'\n{name},{dtString},{date_i}')
    except Exception as e:
        print(f"출석 기록 오류 (Error marking attendance): {e}")


# 'Attendance_Entry' 디렉터리가 있는지 확인 후 생성 (Check and create 'Attendance_Entry' directory)
if not os.path.exists('Attendance_Entry'):
    os.makedirs('Attendance_Entry')

# 파일 이름에는 날짜만 포함 (Only include date in filename)
date = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%y_%m_%d")
header = ("S.NO", "Time", "Date")

try:
    if not os.path.exists(f"Attendance_Entry/Attendance_{date}.csv"):
        with open(f"Attendance_Entry/Attendance_{date}.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(header)
except Exception as e:
    print(f"초기 CSV 생성 오류 (Error creating initial CSV): {e}")

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
    del images  # 인코딩 후 메모리 해제 (Free up memory after encoding)
    print('인코딩 완료 (Encoding Complete)')
except Exception as e:
    print(f"전처리 중 오류 (Error during preprocessing): {e}")

try:
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("비디오 스트림을 열 수 없음 (Error: Could not open video stream).")
        exit()
    
    while True:
        success, img = cap.read()
        if not success or img is None:
            print("비디오 스트림에서 프레임을 읽는 중 오류 (Error: Failed to read frame from video stream).")
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

        cv2.imshow('출석 시스템 (Attendance System)', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except Exception as e:
    print(f"얼굴 인식 중 오류 (Error during face recognition): {e}")
finally:
    cap.release()
    cv2.destroyAllWindows()
