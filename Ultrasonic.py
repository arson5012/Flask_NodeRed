"""초음파"""

import RPi.GPIO as GPIO
import time
from time import sleep
import paho.mqtt.client as mqtt

TRIG_PIN = 23
ECHO_PIN = 24
GPIO_LED = 19
#핀 설정 

def initUltrasonic():
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    #setup 함수 부_메인 부와 합쳐도 무방
    

def controlUltrasonic():
    distance = 0.0
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.03)#0.03초 마다 값 갱신 
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    
    GPIO.output(TRIG_PIN, False)
    
    pulse_start = 0
    pulse_end = 0
    # 루프문에서 받지 않을 수도 있기때문에 초기화

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()



    pulse_duration = pulse_end - pulse_start
    # 보내고 받고

    #distance = pulse_duration * 17000
    # 초음파 속도 약 340m/s, 속도 = 거리 / 시간
    # 보내고 받는 시간 나누기 2, 단위 미터
    # 거리=시간*속도 
    
    distance = (pulse_duration * 34300)/2
    

    #distance = round(distance, 2)
    # 소수점 둘째자리 까지 표기
    # 밑 출력문에서 지정해주기 때문에 무의미 

    return distance



def main():
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(GPIO_LED,GPIO.OUT)
    GPIO.setup(TRIG_PIN,GPIO.OUT)
    GPIO.setup(ECHO_PIN,GPIO.IN)
    # 위에서 지정한 핀을 각각 입/출력으로 지정 

    GPIO.output(TRIG_PIN, False)
    distance = 0.0
    initUltrasonic()#함수부 실행 
    print("초음파 센서를 사용한 인식 시작")

    try:

        while True:

            distance = controlUltrasonic()
            #거리 계산 함수부 실행

            # print("Distance:%.1f mm"%distance)

            if distance <= 100:#1미터=100cm

#                 print("1M 이내입니다 LED ON")
#                 print("거리:%.2fcm" % distance)
                
                dist=str("%.2fcm" % distance)
                # mqtt에서 출력할 결과를 문자열로 형변환
                # 단위와 함께 소수점 두번째 자리까지 출력
                # (하지 않을 경우 너무 지저분 함)
                
                GPIO.output(GPIO_LED, True)
                mqtt.publish("LED/led", "Detected")#Detected
                sleep(0.5)
                #LED ON

            else:

#                 print("인식되지 않았습니다 \n LED OFF")
                dist=str("%.2fcm" % distance)
                # 한국말 표기 안됨 
                # 1미터가 넘어갈 경우 간단하게 mqtt에서 LED OFF문장만 출력 
                GPIO.output(GPIO_LED, False)
                mqtt.publish("LED/led", "Undetected")
                sleep(0.5)
                #LED OFF


    except KeyboardInterrupt:
        GPIO.cleanup()
        # 키보드 인트럭트 실행 후 GPIO 초기화 


if __name__ == '__main__':
    mqtt = mqtt.Client("LED")  # Mqtt Client 오브젝트 생성
    mqtt.connect("125.139.137.12", 1590)  # MQTT 서버에 연결
    main() # 메인부 실행

