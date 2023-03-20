"""기존 카메라"""

import time
import io
import threading
import picamera
import cv2
import sys
import random

def main():
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # 카메라가 작동하지 않으면 실패 메시지 띄움
    if not capture.isOpened():
        print('Video open failed!')
        sys.exit()

    # 보행자 검출을 위한 HOG 기술자 설정
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    while True:
        # frame이라는 변수에 카메라 영상 1프레임씩 받아옴
        ret, frame = Camera.get_frame()

        # 매 프레임마다 보행자 검출
        detected, _ = hog.detectMultiScale(frame) # 사각형 정보를 받아옴
    
        # 검출 결과 화면 표시, 검출된 보행자 주변에 사각형 그려줌
        for (x, y, w, h) in detected:
            c = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            cv2.rectangle(frame, (x, y, w, h), c, 3)
    
        # 매 프레임마다 화면에 보여줌
        cv2.imshow("VideoFrame", frame)
    
        # esc키 누르면 카메라 종료
        if cv2.waitKey(1) == 27:
            capture.release()
            cv2.destroyAllWindows()
            break

class Camera(object):
    thread = None
    frame = None
    last_access = 0

    def initialize(self):
        if Camera.thread is None:
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            camera.resolution = (1285, 640)
            camera.hflip = True
            camera.vflip = True

            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                stream.seek(0)
                cls.frame = stream.read()

                stream.seek(0)
                stream.truncate()

                if time.time() - cls.last_access > 10:
                    break
        cls.thread = None
