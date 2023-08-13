# **(엔비디아 젯슨 나노 4G 디바이스를 사용한 얼굴 기반 출석 시스템)FACE BASED ATTENDANCE SYSTEM USING NVIDIA JETSON Nano 4G DEVICE**

![20230409_100542_1](https://user-images.githubusercontent.com/75832198/230754595-8df2c106-41a3-4782-acce-9d3b63601444.jpg)


## **OBJECTIVE:**

1. 얼굴 기반 출석 시스템은 얼굴 인식 기술을 통합하여 직원 또는 학생의 얼굴 특징을 인식 및 확인하고 자동으로 출석을 기록합니다.  

2. 안면 인식 출퇴근 시스템은 비즈니스에서 직원들이 현장에 있을 때 비접촉 방식으로 직원을 크게 관리할 수 있는 방법입니다.


## **STEPS TO FOLLOW IN THIS PROJECT:**

### **1. Git clone and change directory**

```bash
$ git clone https://github.com/jkf87/AttendanceSystem-Jetsonnano4G_fixed.git
$ cd AttendanceSystem-Jetsonnano4G_fixed
```
원본 코드에서 메모리 관리와 try-except 구문을 추가해서 오류가 날 경우 전체 프로세서가 멈추는 것을 방지합니다.


1. 환경설정하기
- 파이썬 3.6버전 설치
- opencv-python==4.5.2.24 설치
- numpy==1.18.4 설치
- cmake 설치
- dlib 설치
- face_recognition 설치

```
pip install -r requirement.txt
```
해서 설치안되거나 오류나면 오류나는 부분들을 각각 아래에서 별도로 실행해주세요.

```
sudo apt install python3.6
pip install opencv-python==4.5.2.24
python -m pip install numpy==1.18.5 --no-build-isolation
pip install cmake
pip install dlib==19.7.0
pip install face_recognition
```

cmake나 dlib 라이브러리 설치가 안되는 경우 
```
sudo apt-get update
sudo apt-get install -y build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
```
이 부분을 시도(젯슨맘)

2. 폴더에 사진 넣기

Attendance_data에 사진을 영어로 넣어주세요.

3. main.py 실행하기

```
sudo python3 main.py
```

main.py 파일을 실행하면 폴더에 있는 사진을 인코딩하고 이후에 웹캠이 실행되어 얼굴을 인식하게 됩니다. 인식이 되면 Attendance_Entry폴더 안에 csv파일 형태로 매일 저장됩니다. 한번 인식되면 중복으로 체크하지 않도록 하였습니다.
 
---
이 부분은 원본 소스코드의 결과 부분 설명입니다.

## **Result's**

### **Output1: Face recognition**

![vk](https://user-images.githubusercontent.com/75832198/230756159-20a50b3e-a8ee-4c14-9a51-5ac2c8a295ac.png)

### ***Output2: Automatically Attendance stored in Excel sheet***

![csv](https://user-images.githubusercontent.com/75832198/230755026-83840a34-af75-407f-9c64-46880c5928c0.png)

### **5. Remove image in "Attendance_data" folder**

```bash
$ python3 delete_image.py
```
위의 명령어를 실행한 후 터미널에 이름을 입력합니다.

Attendance_data 폴더에 이미지가 삭제되었는지 확인합니다.

## **PROJECT DESCRIPTION:**

1. 요구 사항 파일을 설치합니다.

2. 입력 이미지를 캡쳐하여 "Attendance_data" 폴더에 저장합니다. 

3. 다음 DLIB 라이브러리를 사용하여 주어진 입력 데이터에서 얼굴을 인식합니다.

4. 엑셀 시트에 출석을 입력합니다.

5. 폴더 전체 이미지를 삭제하려면 위의 5번째 단계를 수행합니다.


### **THANK YOU & CREDIT**

1. HarishKumar, Venkatesan (Providing Data and taking demo output video) 
2. BSS.Narayan (Providing the development kit)

## **🤗Happy learning🤗**
