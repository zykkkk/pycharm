# coding=utf-8
import cv2
import numpy as np
import math

cap = cv2.VideoCapture(0)

width = 320
height = 240


def search_ball():
    distance = -1
    times = 0
    while (1):
        ret0, frame = cap.read()
        cv2.imshow('frame', frame)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        blur1 = cv2.GaussianBlur(hsv, (0, 0), 1)
        # define range of red color in HSV
        lower_red = np.array([156, 65, 65])
        upper_red = np.array([180, 255, 255])
        # Threshlod the HSV image to get only red colors
        mask = cv2.inRange(hsv, lower_red, upper_red)
        cv2.imshow('mask', mask)

        # Bitwise-AND mask and original image
        red = cv2.bitwise_and(hsv, hsv, mask=mask)
        cv2.imshow('red', red)

        # 形态学处理
        img1 = cv2.cvtColor(red, cv2.COLOR_HSV2BGR)
        img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(img2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # 做一些形态学操作，去一些小物体的干扰
        img_morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, (1, 1))
        cv2.erode(img_morph, (1, 1), img_morph, iterations=1)

        # dilate = cv2.dilate(img_morph, (1, 1), img_morph, iterations=1)

        blur = cv2.GaussianBlur(img_morph, (0, 0), 1)

        # cv.Smooth(blur, blur, cv.CV_MEDIAN)

        kernel = np.ones((0, 0), np.uint8)

        # canny = cv2.Canny(blur, 0, 250)

        # threshold image
        ret, threshed_img = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)

        # ret, threshed_img = blur
        # find contours and get the external one
        # image, contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # if not find contours, then print"Not find ball"
        if len(contours) == 0 and times > 5:
            print 'Not find ball'
            FindBall = 0
            # return FindBall
            # break
        else:
            n = 0
            minContourArea = 3.0
            maxContourArea = 100.0
            contourTempArea = 0.0

            for c in contours:
                # get the bounding rect
                x, y, w, h = cv2.boundingRect(c)
                print x, y, w, h

                # 过滤太远的噪点,190cm以后的不用识别,主要过滤场外的复杂场景
                if y <= height / 2:
                    n += 1
                    if n == len(contours) and times > 5:
                        FindBall = 0
                        print "Not find ball"
                        # return FindBall
                        # break
                    continue

                # 图片下方的发现点,75cm-190cmq
                elif y >= height / 2:
                    contoursArea = cv2.contourArea(c)
                    print "\nArea:", contoursArea
                    if minContourArea < contoursArea <= maxContourArea:
                        useSensors = False
                        # headAngle = g_motion.getAngles('HeadPitch', useSensors)
                        headAngle = 0
                        center_x = x + w / 2
                        center_y = y + h / 2
                        # print "y: %d" % y
                        # print "h/2: %d" % (h / 2)
                        # distance, angle = calDistanceAndAngle(center_x, center_y, width, height, headAngle[0],AL_kTopCamera)
                        distance, angle = calDistanceAndAngle(center_x, center_y, width, height, headAngle, 0)
                        print 'distance:  ', distance
                        # cv2.imshow('blur1', blur1)
                        # 在下方发现有点之后就停止，因为在腐蚀的时候可能会将一个圆分为几块会出现这种情况
                        # break
            times += 1
            # if distance > 0:
            # break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            # k = cv2.waitKey(0) & 0xFF
            #
            # if k == 27:
            #     break

            # cv2.destroyAllWindows()
            # cv2.waitKey()


# calDistanceAndAngle(center_x,center_y,width,height,headAngle[0],AL_kTopCamera)
def calDistanceAndAngle(cxnum, rynum, colsum, rowsum, Head_angle, cameraID):
    """
    上摄像头找到球后计算距离和角度
    :param cxnum:
    :param rynum:
    :param colsum:
    :param rowsum:
    :param Head_angle:
    :param cameraID:
    :return:
    """
    distx = -(cxnum - colsum / 2)
    disty = rynum - rowsum / 2
    print "disty: %d" % disty
    print "coordinate:", distx, disty   # 复数？
    # print disty

    Picture_angle = disty * 47.64 / 240

    if cameraID == 0:
        h = 0.463
        Camera_angle = 4.7145
        print "Head_angle:", Head_angle

    else:
        h = 0.57
        Camera_angle = 38

    print h, Picture_angle, Camera_angle

    Total_angle = math.pi * (Picture_angle + Camera_angle) / 180 + Head_angle

    print Picture_angle, Total_angle

    d1 = h / math.tan(Total_angle)
    print "distance_y：", d1

    alpha = math.pi * (distx * 60.92 / 320) / 180
    d2 = d1 / math.cos(alpha)
    print 'angle = ', alpha, 'distance = ', d2
    return d2, alpha


search_ball()
