"""main부 flask"""


from board import *
import adafruit_dht
import time
import datetime
import sys
import cv2,os
import numpy as np
import picamera
from flask import Flask, render_template, Response
import paho.mqtt.client as mqtt
import datetime

mqtt = mqtt.Client("sensor")
mqtt.connect("125.139.137.12",1590)
mqtt.loop(2)

app = Flask(__name__, static_url_path='')
#static 폴더 접근 권한 부여


#faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#얼굴 인식 (필요없음)

now=datetime.datetime.now()
#실시간 

if(now.hour<19):
    mqtt.publish("sensor/light","OFF")
else:
    mqtt.publish("sensor/light","ON")
#19시 이후에 가로등 점등

# if (now.hour<5):
#     mqtt.publish("sensor/light","OFF")
# elif (now.hour>20):
#     mqtt.publish("sensor/light","ON")
# # else:
# #     mqtt.publish("sensor/light","OFF")

@app.route('/')
#온습도 센서+flask
def index():
    while True:
        pin=D17
        dhtDevice = adafruit_dht.DHT11(pin,use_pulseio=False)
        try:
            dhtDevice.measure()
            t = dhtDevice.temperature
            time.sleep(0.3)
            h = dhtDevice.humidity
            time.sleep(0.3)


            if(h>=70):
                mqtt.publish("sensor/h","High")
            else:
                mqtt.publish("sensor/h","non")
            
            if(t>=28):
                mqtt.publish("sensor/t","High")
            else:
                mqtt.publish("sensor/t","non")

            #온습도 각각28도 70% 이상이면 LED점등
            
            #tm=str(26)
            #hu=str(50)
	        #임의값 지정


            tm=str(t)
            hu=str(h)
            

            mqtt.publish("sensor/tmp",tm)
            time.sleep(0.1)
            mqtt.publish("sensor/hu",hu)
            time.sleep(0.1)
            
        

            print(tm+"'C"+" "+hu+ "%")

            return render_template('index.html')
        except KeyboardInterrupt:
            GPIO.cleanup()
        except RuntimeError:
            pass
"""       
def gen():
    while True:
        camera = cv2.VideoCapture(0)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320) 
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        time.sleep(0.2)
        lastTime = time.time()*1000.0
        while camera.isOpened():
            try:
                ret, image = camera.read()
                image = cv2.flip(image, 1)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=6)
                
                for (x, y, w, h) in faces:
                    cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
                now = datetime.datetime.now()
                timeString = now.strftime("%Y-%m-%d %H:%M")
                    
                cv2.putText(image, timeString, (10, 25),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                ret, buffer = cv2.imencode('.jpg', image)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except cv2.error:
                pass
        




@app.route('/play')

def play():
    
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')"""

#openCV 부 전부 주석 처리

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port="5823", threaded = True) 
    #디버그 시 static 오류-> 디버그 추가 안함


