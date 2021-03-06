#!/usr/bin/env python
'''
This program takes an image and detects the color of the rectangles in there.
If it is blue, green, red or yellow, it will be counted as valid. At the end, the 
pattern is printed in order.

Program was taken from stackoverflow.com/a/14477677 and then modified in order
to make it more efficient, add coments and fix some parts. All code was made by
 the author in that link with the exception of the lines marked with the tag
*** MODIFICATION.

The *** USER tag in the comments is to point good places where the user 
can modify it for his own purpouses.
'''
import cv2

# *** MODIFICATION: grab an image from the camera
s, image = cam.read()
if s:
	# *** USER: change name of file
	imwrite('cam_image.jpg', image)

img = cv2.imread('rectangles.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Convert image to hsv plane.
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # *** MODIFICATION: changed gray for img

# Binarize the image and detect contours.
edges = cv2.Canny(gray,50,150) # *** MODIFICATION: changed img for gray
contours,hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

# Keep rectanles
res = []

# Go through all contours and find their area. Only continue if it isn't too small (noise).
for cnt in contours:
	if cv2.contourArea(cnt) > 100:
		# Find a rectangle for it
		x,y,w,h = cv2.boundingRect(cnt)
		
		# Find the center of the rectangle
		cx,cy = x+w/2, y+h/2
		
		# Check its color
		color = hsv[cy,cx,0]
		
		# If the color is red, green, tellow or blue put into the list of rectangles.
		if (color < 10 or color > 170):
			res.append([cx,cy,'R'])
		elif(50 < color < 70):
			res.append([cx,cy,'G'])
		elif(20 < color < 40):
			res.append([cx,cy,'Y'])
		elif(110 < color < 130):
			res.append([cx,cy,'B'])
			
# Sort the list by x coordinate.
res = sorted(res, key = lambda res : res [0])

# Print the letters representing the colors of the rectangles
print [x[2] for x in res]
