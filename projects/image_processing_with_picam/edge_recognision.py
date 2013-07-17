#!/usr/bin/env python
import cv
from cv2 import *
import numpy as np
import os

# Set windows to show results
namedWindow("Normal feed", cv.CV_WINDOW_AUTOSIZE)
namedWindow("Edge detection", cv.CV_WINDOW_AUTOSIZE)

# Read from the camera
while True:
 os.system("raspistill -w 400 -h 300 -n -t 0 -o cam_image.jpg")

 # Code from stack overflow
 # Open the image
 image = cv.LoadImage('cam_image.jpg') 

 yuv = cv.CreateImage(cv.GetSize(image),8,3)
	
 # convert to grey
 gray = cv.CreateImage(cv.GetSize(image),8,1)
 cv.CvtColor(image,yuv, cv.CV_BGR2YCrCb)
 cv.Split(yuv,gray, None,None,None)

 # Use canny algorithm for edge detection
 canny = cv.CreateImage(cv.GetSize(image),8,1)
 cv.Canny(gray,canny,50,200)
 
 # Save the image
 cv.SaveImage("Canny.jpg", canny)

 # Show the images
 cv.ShowImage("Normal feed", image)
 cv.ShowImage("Edge detection", canny)	
 waitKey(1)	
	
