# coding=utf-8
import time
import sys
import cv2

a=12
n = 0  # n=10
classfier = cv2.CascadeClassifier("../xml/xml3.xml")  # 来自xml12
img = cv2.imread('../pictures/%d.png' % a)
grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
color = (0, 255, 0)
# 1.2和2分别为图片缩放比例和需要检测的有效点数
landmarks = classfier.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(50, 50))
print(len(landmarks))
# time.sleep(20)
if len(landmarks) > 0:
    # print('find%dfaces' % len(landmarks))
    # time.sleep(1)
    for faceRect in landmarks:  # 单独框出每一个
        x, y, w, h = faceRect
        try:
            print cv2.contourArea(faceRect)
        except Exception ,e:
            print e
        print x,y,w,h
        cv2.rectangle(img, (x - n, y - n), (x + w + n, y + h + n), color, 2)
else:
    print("can't find a face")
    # time.sleep(2)
cv2.imshow('test', img)
cv2.waitKey(2000)
cv2.destroyAllWindows()
