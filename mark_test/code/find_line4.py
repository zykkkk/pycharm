# coding=utf-8
import cv2 as cv
import math

a = 3
number = 0
target = []


def get_theta(line):
    x1, y1, x2, y2 = line
    y2 = float(y2)
    if x1 == x2:
        theta = 90
    else:
        theta = (y2 - y1) / (x2 - x1)
    theta = math.atan(theta)
    return abs(theta)


def line_detect_possible_demo(image):
    global number
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(gray, 50, 150, apertureSize=3)
    # lines = cv.HoughLinesP(edges, 1, math.pi / 180, 100, minLineLength=50, maxLineGap=10)
    lines = cv.HoughLinesP(edges, 1, math.pi / 180, 30, minLineLength=10, maxLineGap=100)

    # print lines
    print len(lines[0])
    for line in lines[0]:
        # print(type(line))
        # print line
        x1, y1, x2, y2 = line
        theta = get_theta(line)
        if 1.5 <= theta <= 1.6:  # 弧度
            print x1, y1, x2, y2
            target.append(x1)
            target.append(x2)
            print 'theta', theta
            cv.line(image, (x1, y1), (x2, y2), (255, 255, 255), 1)
            cv.imshow("line_detect_possible_demo", image)
            number += 1
            # cv.waitKey(0)


img = cv.imread("../mypic/%d.jpg" % a)
cv.namedWindow("Show", cv.WINDOW_AUTOSIZE)
cv.imshow("Show", img)
line_detect_possible_demo(img)
print '线条数', number


def my_event(event, x, y, flags, param):
    if event == cv.EVENT_FLAG_LBUTTON:
        print x


cv.setMouseCallback('Show', my_event)
if len(target) == 4:
    print 'x,y', sum(target) / 4, 240 / 2
cv.waitKey(0)
cv.destroyAllWindows()
