import cv2
import numpy as np

# Load image, grayscale, Otsu's threshold
image = cv2.imread("Img.jpeg")
original = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Dilate with horizontal kernel
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
dilate = cv2.dilate(thresh, kernel, iterations=3)

# Find contours and remove non-diagram contours
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    area = cv2.contourArea(c)
    if w/h > 0.2 and area < 64000 :
        m = cv2.drawContours(image, [c], -1, (0,255,0), 3)
        cv2.imwrite('img_cntr2.png',m)
        cv2.waitKey(0)

# Iterate through diagram contours and form single bounding box
boxes = []
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    boxes.append([x,y, x+w,y+h])

boxes = np.asarray(boxes)
x = np.min(boxes[:,0])
y = np.min(boxes[:,1])
w = np.max(boxes[:,2]) - x
h = np.max(boxes[:,3]) - y

# Extract ROI
cv2.rectangle(image, (x,y), (x + w,y + h), (36,255,12), 3)
ROI = original[y:y+h, x:x+w]

cv2.imshow('image', image)
cv2.imshow('thresh', thresh)
cv2.imshow('dilate', dilate)
cv2.imshow('ROI', ROI)
