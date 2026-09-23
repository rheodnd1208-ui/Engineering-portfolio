# 라즈베리파이 실습 프로젝트

## 1. 기본 정보
- 학번: 2022732052
- 이름: 고대웅
- 작품명: 온도 기반 원격 관제 및 Telegram 경보 시스템

## 2. 선택 기능
- 선택 기능 1: F1 GPIO 출력 제어
- 선택 기능 2: F2 센서 입력
- 선택 기능 3: F5 외부 연동 또는 저장 기능

## 3. 작품 목적

라즈베리파이에 연결된 MPU9250 센서에서 온도 값을 입력받고, 측정된 온도가 설정한 임계값을 초과하면 GPIO 출력 장치를 동작시키는 온도 경보 시스템을 구현하였다.

또한 위험 온도에 도달하거나 정상 온도로 복구될 때 Telegram 메시지를 전송하여 사용자가 원격으로 시스템 상태를 확인할 수 있도록 하였다.

## 4. 사용한 하드웨어

| 구분 | 사용 부품 |
|---|---|
| Raspberry Pi | Raspberry Pi 4 |
| Sensor | MPU9250 센서 모듈 |
| Output device | LED 모듈 |
| 기타 | Galaxy S25+, 점퍼선 |

## 5. 사용한 소프트웨어 및 라이브러리

| 구분 | 내용 |
|---|---|
| 실행 환경 | Python script |
| Python version | Python 3.13.5 |
| 사용 라이브러리 | RPi.GPIO, smbus, imusensor.MPU9250, telegram, asyncio |
| Web framework | 해당 없음 |
| External service or storage | Telegram |

## 6. 전체 시스템 동작 설명

1. GPIO의 모드를 BCM으로 바꾸고 5번핀을 출력핀으로 설정한다.
2. I2C 모듈을 초기화 한다. 임계값을 31.0으로 설정하고 경고 메시지 플래그를 False로 설정한다.
3. 만약 텔레그램 전송 중 오류가 발생하면 "텔레그램 전송 오류: error 원인"이 발송된다.
4. 1초마다 센서에서 온도를 가져오며 이는 터미널에 출력된다.
4. 만약 센서에서 받아온 온도값이 임계값 보다 크면 LED가 켜지며 텔레그램 봇에 경고 메시지를 보낸다.
5. 이후 만약 온도가 임계값보다 낮아지면 온도 복구 메시지가 출력된다.
6. ctrl + c를 누를시 시스템 종료 메시지와 함께 시스템이 종료된다.

## 7. 선택 기능별 구현 증거표

| 선택 기능 | 기능명 | 구현 여부 | 코드 위치 | 영상 시간 | 증거 설명 |
|---|---|---|---|---|---|
| F1 | GPIO 출력 제어 | O | line 11-12, 35-41, 43-48 | 00:35-00:43 | GPIO BCM 모드를 설정하고 GPIO 5번 핀을 출력으로 지정하였다. 온도가 임계값을 초과하면 출력 장치를 켜고, 정상 온도에서는 출력 장치를 끈다. |
| F2 | 센서 입력 | O | line 13-15, 31-33 | 00:20-00:36 | I2C 버스와 MPU9250 센서를 초기화하고, 루프 안에서 센서 값을 읽어 현재 온도를 터미널에 출력한다. |
| F5 | 외부 연동 또는 저장 기능 | O | line 4, 7-9, 20-24, 38-40, 45-47 | 00:34-00:59 | Telegram Bot을 사용하여 위험 온도 도달 시 경고 메시지를 보내고, 정상 온도로 복구되면 복구 안내 메시지를 전송한다. |

## 8. 실행 방법

1. 라즈베리파이에 MPU9250 센서를 연결한다.
2. LED 또는 부저와 같은 출력 장치를 GPIO 5번 핀에 연결한다.
3. 아래 명령어를 통해 프로그램을 실행한다.

```bash
python main.py
```

4. 터미널에 출력되는 온도 값, GPIO 출력 장치의 동작, Telegram 메시지 수신 여부를 확인한다.
5. 프로그램을 종료하려면 Ctrl + C를 누른다.

## 9. 주요 코드 설명

### GPIO 출력 설정

```python
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
```

라즈베리파이의 GPIO 번호 체계를 BCM 방식으로 설정하고, GPIO 5번 핀을 출력 핀으로 사용하도록 설정한다.

### 센서 초기화

```python
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, 0x68)
imu.begin()
```

smbus.SMBus(1)을 사용하여 MPU9250 센서를 초기화한다.

### 센서값 읽기

```python
imu.readSensor()
current_temp = imu.Temp
print(f"temperature: {current_temp:.2f}")
```

MPU9250 센서에서 데이터를 읽고, 현재 온도 값을 가져와 터미널에 출력한다.

### 온도에 따른 GPIO 출력 제어

```python
if current_temp > THRESHOLD_TEMP:
    GPIO.output(5, True)
else:
    GPIO.output(5, False)
```

현재 온도가 임계값보다 높으면 GPIO 5번 핀의 출력 장치를 켜고, 임계값 이하이면 출력 장치를 끈다.

### Telegram 메시지 전송

```python
async def send_message(chat_id, message):
    try:
        await bot.sendMessage(chat_id=chat_id, text=message)
    except Exception as e:
        print(f"텔레그램 전송 오류: {e}")
```

Telegram Bot API를 이용하여 지정된 Chat ID로 메시지를 전송한다. 전송 중 오류가 발생하면 오류 메시지를 터미널에 출력한다.

### 위험 상태 알림

```python
warning_msg = f"[경고] 위험 온도 도달! 현재 온도: {current_temp:.2f} ℃"
await send_message(my_chat_id, warning_msg)
```

온도가 31.0℃를 초과하면 위험 상태로 판단하고 Telegram으로 경고 메시지를 전송한다.

### 정상 복구 알림

```python
normal_msg = f"[안내] 정상 온도 복구. 현재 온도: {current_temp:.2f} ℃"
await send_message(my_chat_id, normal_msg)
```

위험 상태였던 시스템이 정상 온도로 돌아오면 Telegram으로 정상 복구 메시지를 전송한다.

## 10. 구현 결과

프로그램 실행 후 MPU9250 센서에서 온도 값을 읽어 터미널에 출력하였다. 온도가 31.0℃를 초과하면 GPIO 5번 핀에 연결된 출력 장치가 켜지고, Telegram으로 위험 온도 경고 메시지가 전송된다.

온도가 다시 31.0℃ 이하로 내려가면 GPIO 출력 장치가 꺼지고, Telegram으로 정상 온도 복구 메시지가 전송된다.

이를 통해 F1 GPIO 출력 제어, F2 센서 입력, F5 외부 연동 기능이 하나의 시스템 안에서 연결되어 동작함을 확인할 수 있다.

## 11. 한계점 및 개선 가능성

현재 시스템은 온도 임계값이 코드 안에 고정되어 있어 실행 중 사용자가 기준값을 변경하기 어렵다. 향후에는 설정 파일이나 웹 페이지를 통해 임계값을 변경할 수 있도록 개선할 수 있다.

또한 Telegram Bot Token과 Chat ID가 코드 상에 작성되어있기 때문에, github와 같은 곳에 배포나 공유시 주의가 필요하다.
