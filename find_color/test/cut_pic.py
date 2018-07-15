import cv2
import os
import sys
import time

a = 1
filepath = '../../nao_pic/'
for i in os.listdir(filepath):
    img = cv2.imread(filepath + i)
    # x, y, n = img.shape
    # print(x, y)
    x = 600
    y = 1396
    # print(filepath+i)
    # sys.exit()
    img = img[65:x, 0:y/2]  # x high,y weight
    x,y,z=img.shape
    img=cv2.resize(img,(int(x/2),int(y/2)))
    # print(img.shape)
    # time.sleep(1)
    # cv2.imshow('test', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # sys.exit()
    cv2.imwrite(filepath + 'test%d.png' % a, img)
    a += 1
    # sys.exit()
