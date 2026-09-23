import RPi.GPIO as GPIO
import smbus
from imusensor.MPU9250 import MPU9250
import telegram
import asyncio

bot_token = 'YOUR_TELEGRAM_BOT_TOKEN'
my_chat_id = 'YOUR_TELEGRAM_CHAT_ID'
bot = telegram.Bot(token=bot_token)

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT) 
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, 0x68)
imu.begin()

THRESHOLD_TEMP = 31.0 
is_warning_active = False 

async def send_message(chat_id, message):
    try:
        await bot.sendMessage(chat_id=chat_id, text=message)
    except Exception as e:
        print(f"텔레그램 전송 오류: {e}")

async def main():
    global is_warning_active
    
    try:
        while True:
            imu.readSensor()
            current_temp = imu.Temp
            print(f"temperature: {current_temp:.2f}")
            
            if current_temp > THRESHOLD_TEMP:
                GPIO.output(5, True)
                if not is_warning_active:
                    warning_msg = f"[경고] 위험 온도 도달! 현재 온도: {current_temp:.2f} ℃"
                    await send_message(my_chat_id, warning_msg)
                    print('>> 상태: 위험 (알림 발송)')
                    is_warning_active = True
            else:
                GPIO.output(5, False)
                if is_warning_active:
                    normal_msg = f"[안내] 정상 온도 복구. 현재 온도: {current_temp:.2f} ℃"
                    await send_message(my_chat_id, normal_msg)
                    print('>> 상태: 정상 (복구 알림)')
                    is_warning_active = False
            
            await asyncio.sleep(1) 

    except KeyboardInterrupt:
        print('\n시스템 종료 중...')
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    asyncio.run(main())