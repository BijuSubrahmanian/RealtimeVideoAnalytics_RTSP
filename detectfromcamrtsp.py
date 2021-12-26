import cv2
import numpy as np
import os
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

import requests
import json
import cv2


API='https://<inferenceapi>/infer/'

def get_detections(img):
    content_type = "image/jpeg"
    headers = {"content-type": content_type}
    _, img_encoded = cv2.imencode(".jpg", img)
    try:
        resp = requests.post(
            API, data=img_encoded.tobytes(), headers=headers,
            verify ="./tgt-ca-bundle.crt")
        resp.raise_for_status()
        data = resp.json()
        return data
    except requests.exceptions.HTTPError as e:
        print(e.response.text)





#cap = cv2.VideoCapture("rtsp://192.168.0.27:8554/x",cv2.CAP_FFMPEG )
cap=cv2.VideoCapture("rtsp://<username>:<password>@192.168.0.23:554/stream1",cv2.CAP_FFMPEG)
cnt=0
detections="warming up"
#cap=cv2.VideoCapture(0)
while True:
    ret, img = cap.read()
    if ret == True:
    #send frame to Markov for detection
        if cnt == 30:
            detections=get_detections(img)
            cnt=0
        cnt+=1
        print("detections",detections)
        #cv2.putText(img, "detected objects",cv2.FONT_HERSHEY_SIMPLEX,1,(209, 80, 0, 255),3) #font stroke
        cv2.putText(img,
                        detections,
                            (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 255, 0), 2)
        cv2.imshow('live feed', img)
        k = cv2.waitKey(10)& 0xff
        if k == 27:
            break
cap.release()
cv2.destroyAllWindows()

