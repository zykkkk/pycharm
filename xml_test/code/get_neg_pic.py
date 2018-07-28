# coding=utf-8
import os
import cv2
import sys
import time
import os

classfier = cv2.CascadeClassifier("../xml/xml3.xml")
# classfier = cv2.CascadeClassifier("/usr/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml")
filepath = '/home/sl/my/pycharm_workspaces/__pictures__/test1/test_picture/fengjing/'
filepath1 = '/home/sl/my/test_workspaces/xml/test12/neg/'
# a=457
# a=164454
a = 7392
b = 0
# color=(255,0,0)
for l in os.listdir(filepath):
    # print(filepath4+l)
    img0 = cv2.imread(filepath + l)
    try:
        faceRects = classfier.detectMultiScale(img0, scaleFactor=1.2, minNeighbors=3, minSize=(20, 20))
        # print(len(faceRects))
        if len(faceRects) > 0:
            for faceRect in faceRects:  # 单独框出每一张人脸
                time.sleep(0.1)
                x, y, w, h = faceRect
                img = img0[y:y + h, x:x + w]
                try:
                    # print(img.shape)
                    img = cv2.resize(img, (40, 40))
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    cv2.imwrite(filepath1 + '%d.jpg' % a, img)
                    a += 1
                    # sys.exit(0)
                except Exception as e:
                    b += 1
                    print(img.shape)
                    print(a, b, filepath + l, e)
                    # sys.exit()
            # cv2.rectangle(img0, (x - n, y - n), (x + w + n, y + h + n), color, 2)
            # cv2.imshow('test', img0)
            # cv2.waitKey(500)
            # print(len(faceRects))
            print(a, b, l)
            if a >= 8000:
                sys.exit(0)
                # sys.exit()
    except Exception as e:
        print(e, l)
print a, b
