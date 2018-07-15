import cv2
import time
import almath
import sys

# for i in xrange(7):
#     print i,
# print
# print xrange(7)
# for i in range(7):
#     print i,
# print
# print range(7)

# for i in range(14):
#     j = i / 7
#     k = i % 7
#     if j > 0:
#         anger = almath.TO_RAD * (-k * 30 + 90)
#         print anger
#     else:
#         anger = almath.TO_RAD * (k * 30 - 90)
#         print anger

# a='test'
# b='test'
# if a==b:
#     print 'haha'

a=-1
for i in range(8):
    j = i / 4
    k = i % 4
    if j == 0:
        anger = almath.TO_RAD * (k * 30) * a
        print anger
    else:
        anger = almath.TO_RAD * (90-k * 30) * a
        print anger