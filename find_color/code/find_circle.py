import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('test2.png')
# cv2.imshow('test',img)  # 已经读取到图片
# cv2.waitKey(1000)
# cv2.destroyAllWindows()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度图像
# cv2.imshow('test1',gray)  # 灰度图已经存在
# cv2.waitKey(1000)
# cv2.destroyAllWindows()
plt.subplot(121), plt.imshow(gray, 'gray')
plt.xticks([]), plt.yticks([])
# hough transform
# void HoughCircles(InputArray image,OutputArray circles, int method, double dp, double minDist,
#                             double param1=100,double param2=100, int minRadius=0, int maxRadius=0 )
# 第一参数: 图片
# 第二参数: 检测的圆类型
# 第三参数: 使用的方法
# 第四参数: 检测圆心的累加器图像的分辨率于输入图像之比的倒数，且此参数允许创建一个比输入图像分辨率低的累加器。
# 例如，如果dp= 1时，累加器和输入图像具有相同的分辨率。如果dp=2，累加器便有输入图像一半那么大的宽度和高度。
# 第五参数: 为霍夫变换检测到的圆的圆心之间的最小距离，即让我们的算法能明显区分的两个不同圆之间的最小距离。
# 这个参数如果太小的话，多个相邻的圆可能被错误地检测成了一个重合的圆。反之，这个参数设置太大的话，某些圆就不能被检测出来了
# 第六参数: 有默认值100。它是第三个参数method设置的检测方法的对应的参数
# 第七参数: 也有默认值100。它是第三个参数method设置的检测方法的对应的参数
# HoughCircles(image,圆类型,使用的方法,
circles1 = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1,
                            100, param1=100, param2=30, minRadius=0, maxRadius=300)
circles = circles1[0, :, :]  # 提取为二维
circles = np.uint16(np.around(circles))  # 四舍五入，取整
for i in circles[:]:
    cv2.circle(img, (i[0], i[1]), i[2], (255, 0, 0), 5)  # 画圆
    cv2.circle(img, (i[0], i[1]), 2, (255, 0, 255), 10)  # 画圆心

plt.subplot(122), plt.imshow(img)
plt.xticks([]), plt.yticks([])
cv2.imshow('circle',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
