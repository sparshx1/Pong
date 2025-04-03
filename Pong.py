import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

cap=cv2.VideoCapture(0)
#Width
cap.set(3,1250)
#Height
cap.set(4, 750)

#importing all the images
imgBG= cv2.imread("D:/college/study materials/sem 6/AIML/Lab/Project/Images/Table.png")
imgBall= cv2.imread("D:/college/study materials/sem 6/AIML/Lab/Project/ball.png",cv2.IMREAD_UNCHANGED)
imgBoard1= cv2.imread("D:/college/study materials/sem 6/AIML/Lab/Project/Board5.png",cv2.IMREAD_UNCHANGED)
imgBoard2= cv2.imread("D:/college/study materials/sem 6/AIML/Lab/Project/Board6.png",cv2.IMREAD_UNCHANGED)
imgOver= cv2.imread("D:/college/study materials/sem 6/AIML/Lab/Project/GameOver.png",cv2.IMREAD_UNCHANGED)


#Detection of hand
detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

ball_Pos=[100,100]
#speed for x region
speed1=15
#speed for y region
speed2=15
GameOver=False
score=[0,0]


while True:
    _,img= cap.read()
    img=cv2.flip(img,1)
    # Find hands in the current frame
    hands, img = detector.findHands(img, draw=True, flipType=False)
    
    # Putting background image
    # resizing image to fit the background
    imgBG = cv2.resize(imgBG, (img.shape[1], img.shape[0]))
    img = cv2.addWeighted(img, 0.2, imgBG, 0.8, 0)
    
    #
    if hands:
        for hand in hands:
            x,y,w,h=hand['bbox']
            h1,w1,_=imgBoard1.shape
            y1=y - h1//2
            y1=np.clip(y1,25,540)#upper and lower limit of the board
            if hand['type']=="Left":

               # imgBoard1=cv2.resize(imgBoard1,(70,30))
               # imgBoard1=cv2.rotate(imgBoard1,cv2.ROTATE_90_CLOCKWISE)
                img=cvzone.overlayPNG(img,imgBoard1,(40,y1))
                
                if 40<ball_Pos[0]<40+w1 and y1<ball_Pos[1]<y1+h1:
                    speed1=-speed1
                    ball_Pos[0]+=30
                    score[0]+=1
                                
            if hand['type']=="Right":
                img=cvzone.overlayPNG(img, imgBoard2,(1210,y1))
                
                if 1210-50<ball_Pos[0]<1210 and y1<ball_Pos[1]<y1+h1:
                    speed1=-speed1
                    ball_Pos[0]-=30
                    score[1]+=1
#Game is Over
    if ball_Pos[0]<25 or ball_Pos[0]>1220:
        GameOver=True
        
    if GameOver:
        img=imgOver
        cv2.putText(img,str(score[1]+score[0]).zfill(2), (180,225), cv2.FONT_HERSHEY_COMPLEX, 2.5, (255,255,255),5)
        cv2.putText(img,str("Press R to play again"), (185,260), cv2.FONT_HERSHEY_COMPLEX, 0.25, (255,255,255),1)
        
    #if Game is not over 
    else:        
#Ball Movement

        if ball_Pos[1]>=610 or ball_Pos[1]<=25:
            speed2=-speed2
    
        ball_Pos[0] += speed1
        ball_Pos[1] += speed2


        imgBall=cv2.resize(imgBall,(50,50))
     #   print(imgBall.shape)
        #img = cv2.cvtColor(imgBall, cv2.COLOR_BGR2BGRA)
        img=cvzone.overlayPNG(img, imgBall,ball_Pos)
    
        cv2.putText(img,str(score[0]), (300,650), cv2.FONT_HERSHEY_COMPLEX, 3, (255,255,255),5)
        cv2.putText(img,str(score[1]), (900,650), cv2.FONT_HERSHEY_COMPLEX, 3, (255,255,255),5)
        
    cv2.imshow("Image",img)
    key=cv2.waitKey(1)
    if key==ord('r'):
        ball_Pos=[100,100]
        speed1=15
        speed2=15
        GameOver=False
        score=[0,0]
        imgOver= cv2.imread("D:/college/study materials/sem 6/AIML/Lab/Project/GameOver.png",cv2.IMREAD_UNCHANGED)
    
    
