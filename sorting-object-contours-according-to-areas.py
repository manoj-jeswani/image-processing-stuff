#Contours labelled in descending order of areas

import cv2
import numpy as np

# Function we'll use to display contour area

def get_contour_center(c):
    # Places a red circle on the centers of contours
    M = cv2.moments(c)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
 
    return (cx,cy)


def get_contour_areas(contours):
    # returns the areas of all contours as list
    all_areas = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        all_areas.append(area)
    return all_areas

# Load our image
image = cv2.imread('2.jpg')
orginal_image = image


gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

# Find Canny edges
edged = cv2.Canny(gray, 50, 200)

_,contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
print ("Number of contours found = ", len(contours))


# Let's print the areas of the contours before sorting
print( "Contour Areas before sorting",get_contour_areas(contours))

# Sort contours large to small
sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
#sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:3]

print( "Contor Areas after sorting", get_contour_areas(sorted_contours))

# Iterate over our contours and draw one at a time
for i,c in enumerate(sorted_contours):
    cv2.drawContours(orginal_image, [c], -1, (255,0,0), 3)
    cx,cy=get_contour_center(c)
    cv2.putText(orginal_image, str(i+1), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
   


cv2.imshow('Contours by area 1 to n : 1 for largest and n for smallest', orginal_image)

cv2.waitKey(0)
cv2.destroyAllWindows()










