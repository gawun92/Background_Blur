import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from skimage import io
from skimage import data
from skimage.feature import match_template


# From the video, extracting images in each period of time
# saving images wih two format : gray-scale and RGB type.
def generate_frames():
	cap = cv2.VideoCapture('VIDEO.MOV')
	count = 0
	while(cap.isOpened()):
	  ret, frame = cap.read()
	  if (ret == True):
	    if (count%5 == 0):
	        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	        cv2.imwrite('original_Frame_' + str(count) + '.png', frame)
	        cv2.imwrite('Frame_' + str(count) + '.png', gray)
	    if (cv2.waitKey(1) & 0xFF == ord('q')):
	      break
	  else:
	    break
	  count += 1
	cap.release()
	cv2.destroyAllWindows()



# manually setting the window and template.
# template is approximate large size of square 
# which is that template is moving in the range of this square during the whole video. 
# template is an obect, user can set it and save only the template into new image file
# this template picture will be used for the below functions.
def marking_template_and_window():
	img = cv2.imread('Frame_0.png')
	im = np.array(img,  dtype=np.uint8)
	fig,ax = plt.subplots(1)
	# Display the image
	ax.imshow(im)
	# Create a Rectangle patch
	rect = patches.Rectangle((2850,1450),650,690,linewidth=1,edgecolor='r',facecolor='none')
	rect1 = patches.Rectangle((1400,750),2400,1385,linewidth=1,edgecolor='b',facecolor='none')
	ax.add_patch(rect)
	ax.add_patch(rect1)
	plt.savefig('rectangles.png')
	crop = img[1450:1450+690, 2850:2850+650]	 # the location of template
	plt.imsave('crop.png',crop)
	plt.show()



# this is actually using the given template and window
# each of gray scale image is used for match_template
# this image shape is gray scale and its shape is really weird 
# but the brightest spot(location) is highest value and representing
# the template.
def making_matching_temp():
	for i in range(274):
		index = 5*i
		image = cv2.imread('Frame_' + str(index) +'.png', 0) 
		image = image[750:750+1385+5, 1400:1400+2400+5]  # window
		frame = cv2.imread('crop.png', 0)  # template
		coin = frame
		result = match_template(image, coin,pad_input=True) #added the pad_input bool
		io.imshow(result,cmap='gray')
		io.imsave('m_'+str(index)+'.png', result)
		plt.show()



# making_matching_temp() allows user to get match_Template images 
# and this function is saving the location of template in each picture.
# the change of the template location is saved into the array.
# Through this collection of array, it can be used to see how the template was captured with different angles.
# and visualizing its changes with graph.
def remainder():
	X_arr = []
	Y_arr = []
	XY_arr = []
	for i in range(274):
		index = 5*i
		image = cv2.imread('m_'+str(index)+'.png',0)
		i,j = np.unravel_index(image.argmax(), image.shape)
		X_arr.append(i)
		Y_arr.append(j)
		XY_arr.append([j,i])
	plt.plot( Y_arr, X_arr)
	plt.savefig('graph.png')
	plt.show()


	# for now, we know how the templates is changing from the original template's location.
	# and to blur all the background of template, shifting all the picture, based on the location array.
	# just after shifting, combining.
	count = 1
	for i in range(1,274):
		index = 5*i
		image = cv2.imread('original_Frame_'+str(index) +'.png')
		rows  = image.shape[0]
		cols  = image.shape[1]
		M = np.float32([[1,0, -(XY_arr[count][0]-XY_arr[0][0])],[0,1,-(XY_arr[count][1]-XY_arr[0][1])]])
		wA = cv2.warpAffine(image, M, (cols, rows) )
		cv2.imwrite('shift_'+str(index)+'.png', wA)
		count+= 1

	new_image = cv2.imread('original_Frame_0.png')
	new_image = np.int32(new_image)
	for i in range(1,274):
		index = 5*i
		image = cv2.imread('shift_' + str(index) + '.png')
		new_image += np.int32(image)

	new_image = new_image/275
	new_image = np.uint8(new_image)
	cv2.imwrite('new_.png', new_image)

