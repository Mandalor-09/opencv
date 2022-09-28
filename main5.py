def emp(n):
    pass
collist=[[5,107,0,19,255,255],[133,56,0,159,156,255],[57,76,0,100,255,255],[0,50,50,10,255,255],] #hsv value



import cv2

webcam = cv2.VideoCapture(0)
webcam.set(3, 720)
webcam.set(4, 720)
webcam.set(10, 100)
v = cv2.namedWindow('output')
w = cv2.createTrackbar('hmin', 'output', 0, 179, emp)
e = cv2.createTrackbar('hmax', 'output', 179, 179, emp)
r = cv2.createTrackbar('smin', 'output', 0, 255, emp)
t = cv2.createTrackbar('smax', 'output', 255, 255, emp)
y = cv2.createTrackbar('vmin', 'output', 0, 255, emp)
u = cv2.createTrackbar('vmax', 'output', 255, 255, emp)
import numpy as np

while True:
    succes, img = webcam.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hmin = cv2.getTrackbarPos('hmin', 'output')
    hmax = cv2.getTrackbarPos('hmax', 'output')

    smin = cv2.getTrackbarPos('smin', 'output')
    smax = cv2.getTrackbarPos('smin', 'output')
    vmin = cv2.getTrackbarPos('vmin', 'output')
    vmax = cv2.getTrackbarPos('vmin', 'output')
    print(hmin, hmax, smin, smax, vmin, vmax)
    for i in collist:
        lower = np.array([i[0:3]])
        upper = np.array([i[3:]])
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(img, img, mask=mask)
        cv2.imshow('img', result)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
