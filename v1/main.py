from pickletools import uint8
from cv2 import COLOR_BGR2GRAY, COLOR_BGR2HSV, COLOR_BGR2RGB, COLOR_HSV2BGR, COLOR_RGB2BGR, GaussianBlur, bitwise_and
import numpy as np 
from PIL import ImageGrab
import cv2
import time 

def draw_lines(img,lines):
    try:
        for line in lines:
            coords= line[0]
            cv2.line(img,(coords[0],coords[1]),(coords[2],coords[3]),[0,0,255],5)
    except:
        pass

def process_image(original_image):
    bgr = cv2.cvtColor(original_image,COLOR_RGB2BGR)
    hsv = cv2.cvtColor(bgr,COLOR_BGR2HSV)
    lower = np.array([45, 0, 0], np.uint8)
    upper = np.array([55, 200, 200], np.uint8)
    mask = cv2.inRange(hsv,lower,upper)
    filter = bitwise_and(hsv,hsv,mask=mask)
    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(filter, cv2.MORPH_OPEN, kernel)
    edges = cv2.Canny(opening,200,300)

    if int(cv2.__version__[0])>3:
        contours,_= cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    else :
        _,contours,_=cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    for count in contours :
        area = cv2.contourArea(count)
        approx = cv2.approxPolyDP(count,0.02*cv2.arcLength(count,True),True)
        cv2.drawContours(opening, [approx], 0, (255, 0, 0), 5)
    
        rc = cv2.minAreaRect(count)
        box = cv2.boxPoints(rc)

    return opening  


last_time = time.time()
while True:
    screen = np.array(ImageGrab.grab(bbox=(0,300,1024,600)))
    # print(printscreen_pil)
    # printscreen_numpy = np.array(printscreen_pil.getdata(),dtype = 'uint8')\
    # .reshape((printscreen_pil.size[1],printscreen_pil.size[0],3))

    processed_img = process_image(screen)
    cv2.imshow('processed',processed_img)
    # cv2.imshow('window',cv2.cvtColor(screen,cv2.COLOR_BGR2RGB))
    print(time.time()-last_time)
    last_time = time.time()
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows
        break