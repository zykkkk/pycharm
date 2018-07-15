# created by Huang Lu
# 28/08/2016 14:46:31
# Department of EE, Tsinghua Univ.

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# set blue thresh
# lower_blue=np.array([78,43,46])
# upper_blue=np.array([110,255,255])
yellow=[[26, 77, 46],[35, 255, 255]]
lower_blue,upper_blue=np.array(yellow)
kernel_4 = np.ones((4, 4), np.uint8)
while(1):
    # get a frame and show
    ret, frame = cap.read()
    cv2.imshow('Capture', frame)

    # change to hsv model
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # cv2.imshow('test',hsv)

    # get mask
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    cv2.imshow('Mask', mask)

    # detect blue
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow('Result', res)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()