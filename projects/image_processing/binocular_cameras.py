#!/usr/bin/env python
import cv
from cv2 import *

# Code from glowing python
# Keep objects whsoe disparity is above the set threshold
def cut(disparity, image, threshold):
 for i in range(0, image.height):
  for j in range(0, image.width):
   # keep closer object
   if cv.GetReal2D(disparity,i,j) > threshold:
    cv.Set2D(disparity,i,j,cv.Get2D(image,i,j))

# Set cameras. The one at the left should be the one connected
# first to the Raspberry
caml = VideoCapture(0)
camr = VideoCapture(1)

# grab an image from the left camera
s, image = caml.read()
if s:
 imwrite('scene_l.bmp', image)

# grab an image from the right camera
s, image = camr.read()
if s:
 imwrite('scene_r.bmp', image)

# Load each image in grey
left = cv.LoadImage('scene_l.bmp',cv.CV_LOAD_IMAGE_GRAYSCALE)
right = cv.LoadImage('scene_r.bmp',cv.CV_LOAD_IMAGE_GRAYSCALE)

disparity_left = cv.CreateMat(left.height, left.width, cv.CV_16S)
disparity_right = cv.CreateMat(left.height, left.width, cv.CV_16S)

# data structure initialization
state = cv.CreateStereoGCState(16,2)
# running the graph-cut algorithm
cv.FindStereoCorrespondenceGC(left,right,disparity_left,disparity_right,state)

disp_left_visual = cv.CreateMat(left.height, left.width, cv.CV_8U)
cv.ConvertScale(disparity_left,disp_left_visual,-16)

# cutting the object farthest of a threshold
cut(disp_left_visual,left,80)

# Save image if you want to
cv.SaveImage("Binocular_vision.jpg", disp_left_visual)

# Show result
cv.NamedWindow('Disparity map',cv.CV_WINDOW_AUTOSIZE)
cv.ShowImage('Disparity map',disp_left_visual)
cv.WaitKey()
