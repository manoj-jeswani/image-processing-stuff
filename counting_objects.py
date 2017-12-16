'''Tool/Script using which you can find out a perfect combination of : 
Kernel size (width/height) , Threshold (used to produce binary image) , 
divisor and multiplier for average contour size (to get lower and upper 
bound for contour sizes to be taken into consideration)'''

#Command to issue from terminal : python3 <script_name>.py <test_image> <thickness_of_contour_borders>

#Example: python3 counting_objects.py traffic.jpeg 2




import cv2, sys

def fun():
	global img, thresh,w,h,original,thickness,initial,min_size_factor,max_size_factor
	
	#blurring a grayscaled image 
	# w:kernel Width
	# h:Kernel Height
	
	blur = cv2.GaussianBlur(img, (w, h), 0)
	

	# Anyone thresholding scheme can be used

	#This one thresholding scheme requires a threshold value to be supplied : we will find out accuracy of supplied value by varying value using trackbars
	(t, mask) = cv2.threshold(blur, thresh, 255, cv2.THRESH_BINARY)

	#The following three are automatic thresholding schemes in which threshold value is calculated automatically

	# (t, mask)	 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

	# mask = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)

	# mask = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 115, 1)

	
	# showing the binary image
	cv2.imshow("image", mask)

	#binary image contains all the objects of interest (contours of which are to be found) in white colour with a black background 

	# find contours
	(_, contours, _) = cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


	#below is the calculation of average size of contours
	avg = 0
	for c in contours:
		avg += len(c)

	avg /= len(contours)
	res=[]

	#Below is the filtering of contours on basis of their size
	for i,c in enumerate(contours):
		if len(c)>=avg/min_size_factor and len(c)<=max_size_factor*avg:
			res.append(i)

	# res is a list of indices of contours which curve around actual objects of interest 		
			

	# print table of contours and sizes
	print("Found %d objects." % len(res))
	# for (i, c) in enumerate(contours):
	# 	print("\tSize of contour %d: %d" % (i, len(c)))

	# draw contours over the image (a temporary copy of original image)
	cv2.imwrite('temp.jpeg',original)
	tempo = cv2.imread('temp.jpeg',1)

	for i in res:
		cv2.drawContours(tempo, contours, i, (0, 255, 255), thickness)

	# display original image with contours
	cv2.namedWindow("output", cv2.WINDOW_NORMAL)
	cv2.imshow("output", tempo)


	   





#The following functions get executed whenenver a modification in magnitude occurs at respective Trackbars

def adjustThresh(v):
    global thresh
    thresh = v
    fun()
    
def adjustKernelWidth(v):
    global w
    w= v
    fun()


def adjustKernelHeight(v):
    global h
    h = v
    fun()



def adjustMinSizeFactor(v):
    global min_size_factor
    min_size_factor = v
    fun()

def adjustMaxSizeFactor(v):
    global max_size_factor
    max_size_factor = v
    fun()





'''
 * Main program begins here.

'''

# read and save command-line parameters
filename = sys.argv[1]
thickness = int(sys.argv[2])

# read image as grayscale, and blur it
original = cv2.imread(filename)
img = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)



# create the display window and the trackbar
cv2.namedWindow("image", cv2.WINDOW_NORMAL)
thresh = 128
w=5
h=5
min_size_factor=2
max_size_factor=2


#creating and associating trackbars with respective methods
cv2.createTrackbar("thresh", "image", thresh, 255, adjustThresh)
cv2.createTrackbar("kernelw", "image", w, 155, adjustKernelWidth)
cv2.createTrackbar("kernelh", "image", h, 155, adjustKernelHeight)
cv2.createTrackbar("x in (avg/x)", "image", min_size_factor, 20, adjustMinSizeFactor)
cv2.createTrackbar("y in (avg*y)", "image", max_size_factor, 20, adjustMaxSizeFactor)


fun()
cv2.waitKey(0)







