# -*- coding: utf-8 -*-
# 查看所有的方法，或者特殊指定的方法
import cv2


# 查看包含EVENT的函数
events = [i for i in dir(cv2) if 'EVENT' in i]
print(events)
# 查看包含read的函数
for i in dir(cv2):
    if 'read' in i:
        print(i,end=',')
print('')
# print 中使用 if 语句
print([i if 'read' in i else 'no'])
#查看包含read的函数
print([i for i in dir(cv2) if 'read' in i])
# 查看包含mouse的函数
print([i for i in dir(cv2) if 'MOUSE' in i])
print([i for i in dir(cv2) if 'RGB' in i])