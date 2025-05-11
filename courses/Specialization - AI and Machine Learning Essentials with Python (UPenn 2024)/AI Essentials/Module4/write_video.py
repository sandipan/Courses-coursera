from skimage.io import imread 
from skimage.transform import resize
import os
import glob
import numpy as np

output =  'out.avi' # 'out.mp4'
pat = '*.png' #'*.jpg'# '*.png'

width = max([imread(image).shape[0] for image in glob.glob(pat)]) 
height = max([imread(image).shape[1] for image in glob.glob(pat)]) 
	
# Define the codec and create VideoWriter object
#fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
#out = cv2.VideoWriter(output, fourcc, 20, (width, height), True)
#out = cv2.VideoWriter(output, cv2.VideoWriter_fourcc('F','M','P','4'), 20, (width, height))

os.environ['PATH']+=':C:\\Softwares\\ffmpeg\\bin\\'
import skvideo
skvideo.setFFmpegPath("C:\\Softwares\\ffmpeg\\bin\\")
import skvideo.io

fps = 1 #0.5 #2
crf = 17

writer = skvideo.io.FFmpegWriter("outputvideo.mp4", 
	
            inputdict={'-r': str(fps), '-s':'{}x{}'.format(height, width)},
            outputdict={'-r': str(fps), '-c:v': 'libx264', '-crf': str(crf), '-preset': 'ultrafast', '-pix_fmt': 'yuv444p'}
)

for image in sorted(glob.glob(pat)): # os.listdir('.'):

	im = imread(image)[...,:3]
	w, h, c = im.shape
	frame = 255*np.ones((width, height, c), dtype=np.uint8)
	print(w, width, h, height, c)
	if w < width/2 and h < height/2:
		im = resize(im, (width//2, height//2))
		w, h, c = im.shape

	if w % 2 != 0:
		im = im[:-1,:]
	if h % 2 != 0:
		im = im[:,:-1]
	frame[width//2-w//2:width//2+w//2, height//2-h//2:height//2+h//2, :] = im 
	print(frame.shape)
	#cv2.imwrite('p_' + image, frame)
	writer.writeFrame(frame)

writer.close()

print('Done')