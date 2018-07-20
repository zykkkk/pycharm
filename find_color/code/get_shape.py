#coding:utf-8
import cv2
import numpy as np
from cv2 import *
from numpy import *

f4=cv2.imread('test2.jpg')     #读取图像
cv2.imshow('f4',f4)
# a=rgb2gray(f4)          #将彩色图像转换成灰度图像
a = cv2.cvtColor(f4, cv2.COLOR_BGR2GRAY)

# a_size = size(a)
a_size=a.shape
b = np.ones(a_size)

for i in range(1,a_size[1]):
    for j in range(1,a_size[2]):
        if a(i,j)>=0 & a(i,j)<=50:
            b[i,j]=0



# B =[1 1 1 11 1 1 11 1 1 11 1 1 1]  %此模板的选择有待再考虑
B=np.ones((4,4))
# b = imerode(b,B)
erosion = cv2.erode(b, B, iterations=1)  # erode 侵蝕 being small

for i in range(1,a_size[1]):
    for j in range(1,a_size[2]):
        if b[i,j]==0:
            a[i,j]=255
cv2.imshow('a',a)

# bw=edge(a,'prewitt')     #边缘检测   边缘检测结束后发现还是有一些鼓励的小点，不多它们没有形成闭合的曲线
sobelX = cv2.Sobel(a,cv2.CV_64F,1,0)#x方向的梯度
sobelY = cv2.Sobel(a,cv2.CV_64F,0,1)#y方向的梯度
sobelX = np.uint8(abs(sobelX))#x方向梯度的绝对值
sobelY = np.uint8(abs(sobelY))#y方向梯度的绝对值
sobelCombined = cv2.bitwise_or(sobelX,sobelY)#

[L,num] = bwlabel(bw)               #这里已经给每个区域标好号了，使用bwlabel的话会把鼓励的不成闭合曲线的点也算进去
#一些独立点的像素数量是比较少的，所以可以通过检测每一块区域的像素点大小来决定是不是要删除此像素块
for i in range(1,num):
        [r,c]=find(L==i)
        size_L = size([r,c])
        if size_L(1,1)<30:
            L[r,c]=0
L = logical(L)

se = strel('disk',4)   %创造一个平坦的圆盘型结构元素，其半径为2
L = cv2.imclose(L,se)    %关闭图像
[L,num1] = bwlabel(L)
L = rot90(L,3)
L = fliplr(L)
pixel = cell([num1,1])
centre = zeros(num1,2)
size_L = size(L)
for i in range(1,num1):
    [r,c]=find(L==i)
    pixel{i} = [r,c]
    hold on
    mean_pixel = mean(pixel{i})
    centre(i,:) = mean_pixel
    plot(mean_pixel(1,1),mean_pixel(1,2),'r*')
    size_r = size(r)
    distance = zeros(size_r)
    for j = 1:1:size_r(1)
            distance(j) = sqrt((r(j)-mean_pixel(1))^2 + (c(j)-mean_pixel(2))^2)
    end
    p=polyfit((1:size_r(1))',distance,7)
    x = (1:size_r(1))'
    y = p(1)*x.^7 + p(2)*x.^6 + p(3)*x.^5 + p(4)*x.^4 + p(5)*x.^3 + p(6)*x.^2 + p(7)*x.^1 + p(8)
    %plot(x,y)            %对数据进行拟合，因为数据过于杂乱，不好判断
    min_distance = min(distance)
    max_distance = max(distance)
    min_y        =  min(y)
    max_y        =  max(y)
    num_peaks    =  size(findpeaks(-y))
    if(max_distance - min_distance)<= 15 && (max_y - min_y) <= 15
        text(mean_pixel(1,1),mean_pixel(1,2),sprintf('圆形  %d',i))
    elif num_peaks(1) == 2
        text(mean_pixel(1,1),mean_pixel(1,2),sprintf('三角形  %d',i))
    else
        text(mean_pixel(1,1),mean_pixel(1,2),sprintf('矩形  %d',i))
    end
end