"""
Data collection Module
Based on: Teachable Machine, and Hand Sign Detection course for vowels of the American Sign Language
from Computer Vision Zone course
Websites:
https://teachablemachine.withgoogle.com/
https://www.computervision.zone/courses/hand-sign-detection-asl/
"""

# Import libraries
import cv2
import HandTrackingModule_noSkeleton as htm
import numpy as np
import math
import time

# Capture the webcam
cap = cv2.VideoCapture(0)

# Creating the detector
detector = htm.HandDetector(maxHands=1)

# Params
offset = 20
imgSize = 400

# Folder to save the images taking in real-time
folder = "C:/Users/maalvear/PycharmProjects/lse_vowels_gr/Data/otros"
counter = 0


while True:
    # Read the frames from webcam
    success, img = cap.read()
    # Detecting the hand without skeleton
    hands = detector.findHands(img, draw=False)
    # Crop the image once we have the hand
    if hands: # If there is something in the hand
        hand = hands[0]  # Because we only consider one hand

        # Boundary information
        x, y, w, h = hand['bbox']

        # Creating a white matrix with imgSize x imgSize, with data type np.uint8
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8)*255
        # The exactly dimensions for crop the images
        imgCrop = img[y-offset:y+h+offset, x-offset:x+w+offset]  # height initial y, final is y+h, width initial x,
        # final x+w, the previous step creates our boundary box
        # Put the image crop inside the values on the white matrix
        imgCropShape = imgCrop.shape
        #imgWhite[0:imgCropShape[0], 0:imgCropShape[1]] = imgCrop # starting points of the height would be 0, the ending point of the heigth is the
        # height of the image crop imgCropShape[0], in this case. For the width imgCropShape[1]

        # Relation between height and width
        aspectRatio = h/w

        # Fix the height
        if aspectRatio > 1:
            k = imgSize/h
            wCal = math.ceil(k*w)  # Approx the float to the higher integer, e.g. 3.4, round it to 4. This wCal is the caluclated
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize-wCal)/2)  # This is the gap to push forward the image in the center
            imgWhite[:,  wGap:wCal + wGap] = imgResize



        # Fix the width
        else:
            k = imgSize/w
            hCal = math.ceil(k*h)  # Approx the float to the higher integer, e.g. 3.4, round it to 4. This wCal is the caluclated
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize-hCal)/2)  # This is the gap to push forward the image in the center
            imgWhite[hGap:hCal + hGap, :] = imgResize

        cv2.imshow("ImageCrop", imgCrop)
        cv2.imshow("ImageWhite", imgWhite)


    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord("3"):
        counter += 1
        cv2.imwrite(f'{folder}/Image_{time.time()}.jpg', imgWhite)
        print(counter)
