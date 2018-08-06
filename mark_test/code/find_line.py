# coding=utf-8
import cv2
import math
import time

# 0 40 10
# 1 50 5
# 3 40 9
# 4 40 6
# 5 40 6
a = 8
# b=40  # 看到杆子的部分
b = 70  # 看到杆子的全部
img0 = cv2.imread("../pic/%d.jpg" % a)
img = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)  # 貌似可加可不加
img = cv2.GaussianBlur(img, (3, 3), 0)
edges = cv2.Canny(img, 50, 150, apertureSize=3)
# void HoughLines(
#     InputArray image, OutputArray lines, double rho, double theta, int threshold, double srn=0, double stn=0 )
# cv2.HoughLines(
#     image=灰度图,rho=极径 r以像素值为单位的分辨率,
#                      theta=极角 \theta以弧度为单位的分辨率,threshold=最少的的曲线交点,lines=None,srn=None,stn=None)
lines = cv2.HoughLines(edges, 1, math.pi / 180, b)  # 这里对最后一个参数(最小的像素点数)使用了经验型的值
result = img.copy()
target = []
x = []
y = []
t = []
pt = []
ptt = []
# print lines[0]
# time.sleep(5)
for line in lines[0]:
    rho = line[0]  # 第一个元素是距离rho
    theta = line[1]  # 第二个元素是角度theta 极角,弧度
    target_theta = theta / math.pi * 180
    jiao = abs(90 - target_theta)
    if jiao <= 1:
        # print 'theta', target_theta,
        # print 'rho', rho
        x.append(rho * math.cos(theta))
        y.append(rho * math.sin(theta))
        t.append(math.atan((rho * math.sin(theta)) / (rho * math.cos(theta))))
        target.append(line[0])
        # print 'target', target
        # cv2.waitKey(0)

    if (theta < (math.pi / 4.)) or (theta > (3. * math.pi / 4.0)):  # 垂直直线
        # 该直线与第一行的交点
        pt1 = (int(rho / math.cos(theta)), 0)

        # time.sleep(5)
        # 该直线与最后一行的焦点
        pt2 = (int((rho - result.shape[0] * math.sin(theta)) / math.cos(theta)), result.shape[0])
        # 绘制一条白线
        cv2.line(result, pt1, pt2, (255))
        pt.append(pt1)
        ptt.append(pt2)
    else:  # 水平直线
        # 该直线与第一列的交点
        pt1 = (0, int(rho / math.sin(theta)))
        # 该直线与最后一列的交点
        # pt2 = (result.shape[1], int((rho - result.shape[1] * math.cos(theta)) / math.sin(theta)))
        # 绘制一条直线
        # cv2.line(result, pt1, pt2, (255), 1)

cv2.imshow('Canny', edges)
cv2.imshow('Result', result)
targetx = []
# print len(ptt)
for i in ptt:
    # print i
    x2, y2 = i
    targetx.append(x2)
# exit(0)
# targetx.append()
# print 'target',target
# print 'x',x
# print 'y',y
# print 't',t
# print 'dot1',pt
# print 'dot2',ptt
print len(targetx), targetx


def my_event(event, x, y, flags, param):
    if event == cv2.EVENT_FLAG_LBUTTON:
        # print target
        print targetx
        print x, y


cv2.setMouseCallback('Canny', my_event)

cv2.waitKey(0)
# while (1):
# press 'esc' to exit
# if cv2.waitKey(20) & 0xFF == 27:
# if cv2.waitKey(20) & 0xFF == ord('q'):
#         break
