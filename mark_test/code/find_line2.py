# coding=utf-8
import cv2
import numpy as np
import matplotlib.pyplot as plt

a = 0
img = cv2.imread('../mypic/%d.jpg' % a)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度图像
# open to see how to use: cv2.Canny
# http://blog.csdn.net/on2way/article/details/46851451
edges = cv2.Canny(gray, 50, 200)
plt.subplot(121), plt.imshow(edges, 'gray')
plt.xticks([]), plt.yticks([])
# hough transform
lines = cv2.HoughLines(edges, 1, np.pi / 180, 160)
lines1 = lines[:, 0, :]  # 提取为为二维
for rho, theta in lines1[:]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 1)

plt.subplot(122), plt.imshow(img, )
plt.xticks([]), plt.yticks([])
