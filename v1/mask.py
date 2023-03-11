import numpy as np
from PIL import ImageGrab
import cv2

while True:
    screen = np.array(ImageGrab.grab(bbox=(24,300,1000,600)))
    lower = np.array([45, 50, 100], np.uint8)
    upper = np.array([65, 120, 200], np.uint8)
    rgb = cv2.cvtColor(screen,cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(rgb,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,lower,upper)
    res = cv2.bitwise_and(screen,screen,mask=mask)
    edges = cv2.Canny(res,150,100)

    cv2.imshow("res",edges)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows
        break
