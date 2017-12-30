# issue to solve :: remove redundancy in output :: a lot of same face images appearing in output

# command to execute::
 
# python3 extract-heads-from-video.py video-file.mp4 a b

# where video-file.mp4 has resolution a*b like 480*360 or 1280*720


import numpy
import cv2
import sys



face_classifier = cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')

def face_detector(img, size=0.5):
    global cnt
    # Convert image to grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    rows,cols=gray.shape
    faces = face_classifier.detectMultiScale(gray, 1.2, 4)
    if faces is ():
        return img
    
    for (x,y,w,h) in faces:
        # x = x - 30
        # w = w + 30
        y = y - 30
        h = h + 30
        
        
        black=numpy.zeros((rows,cols,3),dtype='uint8')

        cv2.rectangle(black,(x,y),(x+w,y+h),(255,255,255),-1)
        black=cv2.bitwise_and(img,black)
        image_name="extracted_heads/head-"+str(cnt)+".png"
        cnt=cnt+1
        cv2.imwrite(image_name,black)
       
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        
    return img






A=int(sys.argv[2])
B=int(sys.argv[3])
video_path=str(sys.argv[1])

FFMPEG_BIN = "ffmpeg" # on Linux ans Mac OS

import subprocess as sp

command = [ FFMPEG_BIN,
            '-i', video_path,
            '-f', 'image2pipe',
            '-pix_fmt', 'bgr24',
            '-vcodec', 'rawvideo', '-']
pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**9)




cv2.namedWindow('Face Extractor',cv2.WINDOW_NORMAL)

cnt=1
ls=[]
threshold=210
while True:


    raw_image = pipe.stdout.read(A*B*3)
    image =  numpy.fromstring(raw_image, dtype='uint8')
    frame = image.reshape((B,A,3))

    cv2.imshow('Face Extractor', face_detector(frame))

    if cv2.waitKey(1) == 13: #13 is the Enter Key
        break    
    



pipe.stdout.flush()


cv2.waitKey()
cv2.destroyAllWindows()

