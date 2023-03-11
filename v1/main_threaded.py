from concurrent.futures import thread
from inflection import dasherize
import numpy as np
from PIL import ImageGrab
import cv2
from movement import PressKey, ReleaseKey , W,A,S,D
import threading
import time

final_diffrence = 0

def generate_diff():
    x_coordinates_contour = [0,0,0,0]
    y_coordinates_contour = [0,0,0,0]
    x_coordinates_bbox = [0,0,0,0]
    y_coordinates_bbox = [0,0,0,0]

    midx = 0
    midy = 0

    global final_diffrence

    def image_operations(roimain,kernel):
        lower = np.array([35, 50, 100], np.uint8)
        upper = np.array([65, 120, 200], np.uint8)
        rgb = cv2.cvtColor(roimain,cv2.COLOR_RGB2BGR)
        hsv = cv2.cvtColor(rgb,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv,lower,upper)
        res = cv2.bitwise_and(roimain,roimain,mask=mask)

        opening = cv2.morphologyEx(res,cv2.MORPH_OPEN,kernel)
        edges = cv2.Canny(opening,150,100)
        
        cv2.imshow('opening',cv2.cvtColor(opening,cv2.COLOR_BGR2RGB))

        return edges

    def contour_detection(roimain,edges):
        global box
        if int(cv2.__version__[0])>3:
            contours,_=cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        else :
            _,contours,_=cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        for count in contours:
            area = cv2.contourArea(count)
            approx = cv2.approxPolyDP(count,0.02*cv2.arcLength(count,True),True)
            # cv2.drawContours(roimain, [approx], 0, (0, 0, 0), 5)sss
        
            rc = cv2.minAreaRect(count)
            box = cv2.boxPoints(rc)

            return box

    def bounding_box(screen,box):
        # x1
        x_coordinates_contour[0]= int(box[0][0])
        # x2
        x_coordinates_contour[1]= int(box[1][0])
        # x3
        x_coordinates_contour[2]= int(box[2][0])
        # x4
        x_coordinates_contour[3]= int(box[3][0])

        # y1
        y_coordinates_contour[0]= int(box[0][1])
        # y2
        y_coordinates_contour[1]= int(box[1][1])
        # y3
        y_coordinates_contour[2]= int(box[2][1])
        # y4
        y_coordinates_contour[3]= int(box[3][1])

        # (x1+x3)/2
        mid_x1 = ((x_coordinates_contour[0]+x_coordinates_contour[1])/2)
        
        # (x2+x4)/2
        mid_x2 = ((x_coordinates_contour[3]+x_coordinates_contour[2])/2)

        # (y1+y3)/2
        mid_y1 = ((y_coordinates_contour[3]+y_coordinates_contour[0])/2)
        
        # (y2+y4)/2
        mid_y2 = ((y_coordinates_contour[1]+y_coordinates_contour[2])/2)

        # final contour midpoint
        midx = (mid_x1+mid_x2)//2
        midy = (mid_y1+mid_y2)//2

        # print(midx)
        width = x_coordinates_contour[2]-x_coordinates_contour[0]
        height = y_coordinates_contour[3]- y_coordinates_contour[0]

        x_coordinates_bbox[0] = int(x_coordinates_contour[0]-width)
        x_coordinates_bbox[1] = int(x_coordinates_contour[1]-width)
        x_coordinates_bbox[2] = int(x_coordinates_contour[2]+width)
        x_coordinates_bbox[3] = int(x_coordinates_contour[3]+width)

        y_coordinates_bbox[0] = int(y_coordinates_contour[0])
        y_coordinates_bbox[1] = int(y_coordinates_contour[1]-(height*2))
        y_coordinates_bbox[2] = int(y_coordinates_contour[2]-(height*2))
        y_coordinates_bbox[3] = int(y_coordinates_contour[3])

        start = (x_coordinates_bbox[0],y_coordinates_bbox[1])
        end = (x_coordinates_bbox[2],y_coordinates_bbox[3])

        cv2.rectangle(screen,end,start,(0,0,255),3)

        diffrence = 0
        diffrence = 512-midx # negetive means right , positive means left
        # print(midx)
        # print(diffrence)
        return diffrence
    
    for x in list(range(4))[::-1]:
        print(x)
        time.sleep(1)

    while True:
        screen = np.array(ImageGrab.grab(bbox=(24,300,1000,600)))

        kernel = np.ones((10,10),np.uint8)
        edges = image_operations(screen,kernel)
        box = contour_detection(screen,edges)
        try:
            final_diffrence = 0
            final_diffrence = bounding_box(screen,box)
        except:
            pass

        cv2.imshow('window',cv2.cvtColor(screen,cv2.COLOR_BGR2RGB))
        # print(time.time()-last_time)
        last_time = time.time()

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows
            break

def actions():
    global final_diffrence
    def straight():
        PressKey(W)
        ReleaseKey(A)
        ReleaseKey(D)
    def left(final_diffrence):
        PressKey(A)
        print("left")
        time.sleep(final_diffrence/1000)
        ReleaseKey(A)
        ReleaseKey(W)
        ReleaseKey(D)
    def hardleft():
        PressKey(A)
        PressKey(S)
        ReleaseKey(W)
        ReleaseKey(A)
    def right(final_diffrence):
        PressKey(D)
        print("right")
        time.sleep(final_diffrence/1000)
        ReleaseKey(D)
        ReleaseKey(W)
        ReleaseKey(A)
    def hardright():
        PressKey(D)
        PressKey(S)
        ReleaseKey(W)
        ReleaseKey(A)
    def brake():
        PressKey(S)
        ReleaseKey(W)
        ReleaseKey(A)
        ReleaseKey(D)
    
    while True:
        # print(final_diffrence)
        if final_diffrence < -20:
            right(-final_diffrence)
        if final_diffrence == 0:
            pass
        if final_diffrence > 20:
            left(final_diffrence)

t1 = threading.Thread(target=generate_diff)
t2 = threading.Thread(target=actions)


t1.start()
t2.start()
