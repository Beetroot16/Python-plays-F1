from grabscreen import grab_screen
import cv2
import time as t
import numpy as np
from directkeys import PressKey,ReleaseKey, W, A, S, D
from getkeys import key_check

# for i in list(range(4))[::-1]:
#     print(i+1)
#     time.sleep(1)

# last_time = time.time()

lower= np.array([50,70,70])  # Sunset
upper = np.array([75,250,250]) # Sunset

kernel = np.ones((5,5),np.uint8)

def left(time):
    PressKey(A)
    t.sleep(time)
    ReleaseKey(A)
    ReleaseKey(D)

def right(time):
    PressKey(D)
    t.sleep(time)
    ReleaseKey(D)
    ReleaseKey(A)

def straight(time):
    PressKey(W)
    t.sleep(time)
    ReleaseKey(W)

def release():
    ReleaseKey(S)
    ReleaseKey(W)

def brake():
    PressKey(S)
    t.sleep(0.05)
    ReleaseKey(S)
    ReleaseKey(W)

def no_keys():
    ReleaseKey(A)
    ReleaseKey(D)

counter = 0

diffrence = 0

paused = False

while not paused:
    screen = grab_screen(region=(188,400,788,600))
    # cv2.namedWindow("Hehe")   
    # cv2.moveWindow("Hehe", 1000,400) 
    # screen = cv2.resize(screen, (162,67))
    hsv = cv2.cvtColor(screen,cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(screen,screen, mask= mask)
    # bgr = cv2.cvtColor(opening,cv2.COLOR_HSV2BGR)
    gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)

    ret,thres = cv2.threshold(opening, 120, 255, cv2.THRESH_BINARY)

    whitearr = np.where(thres==255)

    try:
        # cv2.circle(screen,(whitearr[1][-1],whitearr[0][-1]),1,(0,255,255),10)
        # print(whitearr[0][0])
        cv2.rectangle(screen,(whitearr[1][0],whitearr[0][0]),(whitearr[1][-1],whitearr[0][-1]),(255,255,255),1)
        # print(whitearr[0][0],whitearr[1][0])

        midx = whitearr[1][0] + (whitearr[1][-1] - whitearr[1][0])/2
        midy = whitearr[0][0] + (whitearr[0][-1] - whitearr[0][0])/2

        diffrence = 300-midx
        # print(diffrence)
        cv2.circle(screen,(int(midx),int(midy)),1,(0,255,255),10)
        # print(mid)ddd
    except:
        print("release")
        release()
    
        if counter > 10:
            brake()
            print("Brake")
            counter -= 2
        
        if counter < 0:
            counter = 0
    
    print(abs(diffrence),counter)

    if diffrence > 100:
        left(diffrence/800)
    if diffrence < -100: 
        right(-(diffrence/800))
    else:
        counter += 1
        if diffrence > 10:
            straight(abs(5/diffrence))
        else: 
            straight(0.1)


    keys = key_check()
    
    # print(counter)
    
    cv2.imshow("Hehe",thres)
    cv2.imshow("Haha",res)

    if 'T' in keys:
        if paused:
            paused = False
            print('unpaused!')
            t.sleep(1)
        else:
            print('Pausing!')
            paused = True
            t.sleep(1)
    # cv2.imshow("Haha",screen)

    # print(60/(time.time()-last_time))
    # last_time = time.time()
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows
        break