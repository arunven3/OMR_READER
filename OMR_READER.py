import cv2
import numpy as np

threasholdValue = 1000 # VALUE DETERMINE APPROXIMATE CIRCLE COLOURED VALUE
pathImage = "C:/Users/venar/Downloads/newt1.jpg"
heightImg = 700
widthImg  = 700
questions=10
choices=4
ans= [2,0,2,3,2,0,2,3,4,2]

def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2)) # REMOVE EXTRA BRACKET
    myPointsNew = np.zeros((4, 1, 2), np.int32) # NEW MATRIX WITH ARRANGED POINTS
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]  #[0,0]
    myPointsNew[3] =myPoints[np.argmax(add)]   #[w,h]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]  #[w,0]
    myPointsNew[2] = myPoints[np.argmax(diff)] #[h,0]
    return myPointsNew

def rectContour(contours):
    rectCon = []
    for i in contours:
        area = cv2.contourArea(i)
        if area > 50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if len(approx) == 4:
                rectCon.append(i)
    rectCon = sorted(rectCon, key=cv2.contourArea,reverse=True)
    return rectCon

def getCornerPoints(cont):
    peri = cv2.arcLength(cont, True) # LENGTH OF CONTOUR
    approx = cv2.approxPolyDP(cont, 0.02 * peri, True) # APPROXIMATE THE POLY TO GET CORNER POINTS
    return approx

def splitBoxes(img, questions, choices):
    rows = np.vsplit(img, questions)
    boxes=[]
    for r in rows:
        cols= np.hsplit(r,choices)
        for box in cols:
            boxes.append(box)
    return boxes

img = cv2.imread('omrt1.jpg')
img = cv2.resize(img, (widthImg, heightImg)) # RESIZE IMAGE
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # CONVERT IMAGE TO GRAY SCALE
imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1) # ADD GAUSSIAN BLUR
imgCanny = cv2.Canny(imgBlur,10,70) # APPLY CANNY

try:
    imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # FIND ALL CONTOURS
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10) # DRAW ALL DETECTED CONTOURS
    rectCon = rectContour(contours) # FILTER FOR RECTANGLE CONTOURS
    biggestPoints= getCornerPoints(rectCon[0]) # GET CORNER POINTS OF THE BIGGEST RECTANGLE

    if biggestPoints.size != 0 : # BIGGEST RECTANGLE WARPING
        biggestPoints=reorder(biggestPoints) # REORDER FOR WARPING
        cv2.drawContours(imgBigContour, biggestPoints, -1, (0, 255, 0), 20) # DRAW THE BIGGEST CONTOUR
        pts1 = np.float32(biggestPoints) # PREPARE POINTS FOR WARP
        pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
        matrix = cv2.getPerspectiveTransform(pts1, pts2) # GET TRANSFORMATION MATRIX
        imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg)) # APPLY WARP PERSPECTIVE

        # APPLY THRESHOLD
        imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY) # CONVERT TO GRAYSCALE
        imgThresh = cv2.threshold(imgWarpGray, 170, 255,cv2.THRESH_BINARY_INV )[1] # APPLY THRESHOLD AND INVERSE
        boxes = splitBoxes(imgThresh, questions, choices) # GET INDIVIDUAL BOXES
        countR=0
        countC=0
        boxIndex = 0
        myIndex = []

        for image in boxes:
            boxIndex +=1
            blackPixels = (np.sum(image == 255)) # FIND BLACK PIXELS INSIDE BOXES

            if blackPixels > threasholdValue : # COMPARE BLACK PIXELS WITH THRESHOLD VALUES
                marked = boxIndex % 4
                myIndex.append(4 if boxIndex % 4 == 0 else marked)

        print("USER ANSWERS", myIndex)
        correctAnswers=0

        for x in range(0, questions):
             if ans[x] == myIndex[x]: # FIND CORRECT ANSWER
                 correctAnswers +=1

        score = (correctAnswers / questions) * 100  # FINAL GRADE
        print("CORRECT ANSWERS", correctAnswers)
        print("SCORE",score)

except Exception as e:
    print(str(e))