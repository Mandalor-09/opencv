
import cv2 as cv
import numpy as np

widthImg=200
heightImg =300
def trackbar():
    wind=cv.namedWindow('trackbar')
    cv.resizeWindow('trackbar',360,240)
    cv.createTrackbar('treshhold width','trackbar',200,255)
    cv.createTrackbar('treshhold height','trackbar',200,255)
    while True:
        t1=cv.getTrackbarPos('treshold width','trackbar')
        t2=cv.getTrackbarPos('treshold height','trackbar')
        return t1,t2

def processing(img):
    img=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    img=cv.GaussianBlur(img,(7,7),1)
    img=cv.Canny(img,200,200)
    kernel = np.ones((5,5),np.uint8)
    #img=cv.morphologyEx(img,cv.MORPH_CLOSE,kernel,iterations=3)
    img=cv.dilate(img,kernel,2)
    img=cv.erode(img,kernel,1)
    t1,t2=trackbar()
    treshold,img=cv.threshold(img,t1,t2,cv.THRESH_BINARY)
    return img

def countours(img):
    biggest=np.array([])
    maxarea=0
    contours ,hierarchy=cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        area=cv.contourArea(cnt)
        if area>5000:
            #cv.drawContours(img,cnt,-1,(255,0,255),2) #contours are the corner point
            peri=cv.arcLength(cnt,True)
            approx=cv.approxPolyDP(cnt,0.02*peri,True) #approximation of corner point
            if area>maxarea and len(approx)==4:
                biggest=approx
                maxarea=area
            #x,y,w,h=cv.boundingRect(biggest)
    cv.drawContours(img,biggest,-1,(255,0,255),20)
    print(biggest)
    return biggest,maxarea

def re_order_of_biggestpoints(mypoint):
    mypoint=mypoint.reshape((4,2))
    newpoint=np.zeros((4,1,2),np.int32)
    add=np.sum(newpoint,axis=1)
    diff=np.diff(newpoint,axis=1)
    newpoint[0]=mypoint[np.argmin(add)]
    newpoint[1]=mypoint[np.argmin(diff)]
    newpoint[2]=mypoint[np.argmax(diff)]
    newpoint[3]=mypoint[np.argmax(add)]
    return newpoint

def warp(img,biggest):
    #biggest,maxarea=countours(img)
    if biggest.size!=0:
 
        w1=re_order_of_biggestpoints(biggest)
        cv.drawContours(img,w1,-1,(255,0,255),2)
        point1=np.float32(w1)
        point2=np.float32([0,0],[widthImg,0],[0,heightImg],[widthImg,heightImg])
        matrix=cv.getPerspectiveTransform(point1,point2)
        warp_img=cv.warpPerspective(img,matrix,(widthImg,heightImg))
        return warp_img
        img=warp_img[20:widthImg-20,20:heightImg-20]
        img=cv.cvtColor(img,cv.COLOR_BAYER_BG2GRAY)
        return img



    
res=cv.resize(img,(widthImg,heightImg))
imgtres=processing(img)
biggest=countours(imgtres)
print(biggest)
warp(img,biggest)
cv.waitKey(0)

