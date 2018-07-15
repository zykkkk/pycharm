# -*- coding: utf-8 -*-

import cv2
import numpy as np

#mouse callback function
# 双击画圆
def draw_circle(event,x,y,flags,param):
    if event==cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img,(x,y),100,(255,0,0),-1)

# 单击画圆
def my_event(event,x,y,flags,param):
    if event==cv2.EVENT_FLAG_LBUTTON:
        cv2.circle(img,(x,y),100,(255,0,0),-1)
def my_event2(event,x,y,flags,param):
    if event==cv2.EVENT_FLAG_LBUTTON:
        print('RGB:',img[x,y],'   ','GSV:',HSV[x,y])

# 创建图像与窗口并将窗口与回调函数绑定
img=np.zeros((512,512,3),np.uint8)
img=cv2.imread('../test_picture/color.jpg')
HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # 把BGR图像转换为HSV格式
cv2.namedWindow('image')
# cv2.setMouseCallback('image',draw_circle)
cv2.setMouseCallback('image',my_event2)

while(1):
    cv2.imshow('image',img)
    # press 'esc' to exit
    if cv2.waitKey(20)&0xFF==27:
        break
    # else:
    #     print(cv2.waitKey(20)&0xFF)
cv2.destroyAllWindows()