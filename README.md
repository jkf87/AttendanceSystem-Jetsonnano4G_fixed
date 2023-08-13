# **FACE BASED ATTENDANCE SYSTEM USING NVIDIA JETSON AGX XAVIER DEVICE**

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
메모리 관리를 위해 1시간마다 메모리를 비워줍니다.
try-except 구문을 추가해서 오류가 날 경우 전체 프로세서가 멈추는 것을 방지합니다.

cmake나 dlib 라이브러리 설치가 안되는 경우 
```
sudo apt-get update
sudo apt-get install -y build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
```
이 부분을 참고하세요. (젯슨맘)



### **2. Install prerequisite library using requirement file**

```bash

$ pip3 install -r requirement.txt

```
Check that Opencv,numpy,dlib,cmake, and datetime are installed on your AGX device (Packages).

### **3. Take a picture of your input and save it to the "Attendance_data" folder.**

```bash
$ python3 initial_data_capture.py
```
위의 명령어를 실행한 후 터미널에 이름을 입력합니다.

초기 이미지가 '출석_데이터' 폴더에 저장되었는지 확인합니다.

### **4. Attendance system (Main script)**

```bash
$ bash run.sh

or

$ python3 main.py
```

![b](https://user-images.githubusercontent.com/75832198/230757347-01e0a9a9-5799-4fd0-80e4-69de74837703.png)


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
