# coding:utf-8

import cv2


#mouse callback function
# 获取HSV值
def my_event(event,x,y,flags,param):
    if event==cv2.EVENT_FLAG_LBUTTON:
        print
        print x,y
        print('RGB:',frame[x,y],'   ','HSV:',HSV[x,y])

cap = cv2.VideoCapture(0)
cv2.namedWindow('Capture')
cv2.setMouseCallback('Capture',my_event)
while(1):
    ret, frame = cap.read()
    x, y, i = frame.shape
    # x1 = x / 100 + 1
    # y1 = y / 100 + 1
    # x2 = round(x1) * 100
    # y2 = round(y1) * 100
    # frame = cv2.resize(frame, (x2, y2))
    # frame = cv2.resize(frame, (640, 480))
    # cv2.namedWindow('Capture')
    cv2.imshow('Capture', frame)
    # cv2.resizeWindow('Capture',x,y)
    HSV=cv2.cvtColor(frame,cv2.COLOR_RGB2HSV)
    cv2.namedWindow('test')
    cv2.imshow('test',HSV)
    # press 'esc' to exit
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()