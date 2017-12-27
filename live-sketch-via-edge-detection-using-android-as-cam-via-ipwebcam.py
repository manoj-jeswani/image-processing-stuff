# Live sketch from cam using edge detection technique

import cv2
import numpy as np
import urllib.request


# Our sketch generating function
def sketch(image):
    # Convert image to grayscale
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Clean up image using Guassian Blur
    img_gray_blur = cv2.GaussianBlur(img_gray, (5,5), 0)
    
    # Extract edges
    canny_edges = cv2.Canny(img_gray_blur, 10, 70)
    
    # Do an invert binarize the image 
    ret, mask = cv2.threshold(canny_edges, 70, 255, cv2.THRESH_BINARY_INV)
    return mask



stream = urllib.request.urlopen('http://192.168.43.1:8080/video') #here use your server ip/video
bytes = bytes()

while True:
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]
        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)


        cv2.imshow('Our Live Sketcher', sketch(frame))
        if cv2.waitKey(1) == 13: #13 is the Enter Key
            break
        
# Release camera and close windows
cap.release()
cv2.destroyAllWindows()