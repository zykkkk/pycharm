# Python program to illustrate HoughLine
# method for line detection
import cv2
import numpy as np

a = 8
n1 = n2 = 1
length_of_line = 70
y=[-20,-40]
x=[0,0]
lines=[]
lines_num=0
nums=0


def my_event(event, x1, y1, flags, param):
    if event == cv2.EVENT_FLAG_LBUTTON:
        print('x',x)
        print('y',y)
        print x1,y1


# Reading the required image in
# which operations are to be done.
# Make sure that the image is in the same
# directory in which this python program is
img = cv2.imread('../pic/%d.jpg' % a)
cv2.imshow('img0',img)
# length_of_line = 400
# Convert the img to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply edge detection method on the image
edges = cv2.Canny(gray, 50, 150, apertureSize=3)
cv2.imshow('edges', edges)
# This returns an array of r and theta values
while lines_num != 2 or 5 <= abs(y[0]-y[1]):
    nums=lines_num=0
    print('there')
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, length_of_line, maxLineGap=20)
    length_of_line += 1
    for line in lines:
        x1, y1, x2, y2 = line[0]
        theta = abs((y2 - y1) / (x2 - x1))
        if theta > 2 or x2 == x1:
            if nums==2:
                continue
            if y2>y1:
                x[nums] = x2
                y[nums] = y2
            else:
                x[nums] = x1
                y[nums] = y1
            nums+=1
            print('x1,y1,x2,y2',x1,y1,x2,y2)
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            lines_num+=1
            # cv2.imshow('img',img)
            # cv2.waitKey(0)
    print('y[0],y[1]',y[0],y[1])
    if length_of_line >= 120:
        print('length_of_line error')
        exit(-1)
print('len lines',len(lines))
# cv2.waitKey(200)
# The below for loop runs till r and theta values
# are in the range of the 2d array
# for line in lines:
#     x1, y1, x2, y2 = line[0]
#     theta = abs((y2 - y1) / (x2 - x1))
#     if theta > 2 or x2 == x1:
#         print('line', line)
#         if x2 != x1:
#             # (y2-y1)/(x2-x1)=(y2-y)/(x2-x)
#             y3 = 0
#             y4 = 240
#             x3 = x2 - (y2 - 0) / (y2 - y1) * (x2 - x1)
#             x4 = x2 - (y2 - 240) / (y2 - y1) * (x2 - x1)
#         else:
#             print('else')
#             x3 = x4 = x1
#             y3 = 0
#             y4 = 240
#         print('x3,y3,x4,y4', x3, y3, x4, y4)
#         cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
#         # cv2.line(img, (x3, y3), (x4, y4), (0, 0, 255), 2)
#         print('success %d times' % n1, theta, line[0])
#         n1 += 1
#     else:
#         # print('failed %d times '%n2,theta,line[0])
#         # cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
#         n2 += 1

# All the changes made in the input image are finally
# written on a new image houghlines.jpg
# cv2.imwrite('houghlines3.jpg', img)
print('n1,n2', n1, n2)
print('x',x)
print('width',abs(x[1]-x[0]))
cv2.imshow('img', img)
cv2.setMouseCallback('img0', my_event)
cv2.setMouseCallback('img', my_event)
cv2.setMouseCallback('edges', my_event)
cv2.waitKey(0)
