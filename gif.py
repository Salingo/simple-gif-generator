import os
import sys
import numpy as np
from PIL import Image, ImageChops
from moviepy.editor import VideoFileClip

SOURCE_FOLDER = sys.argv[-2]
VIDEO_MODE = int(sys.argv[-1])
TRIM_GROUP_MODE = False

''' Trim all images in the SOURCE_FOLDER by the common minimum bbox '''
def trim_group(imgs):
	bboxs = []
	for img in imgs:
		bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
		diff = ImageChops.difference(img, bg)
		bbox = diff.getbbox()
		bboxs.append(bbox)
	bboxs = np.array(bboxs)
	common_bbox = np.zeros((4))
	common_bbox[0] = np.min(bboxs, axis=0)[0]
	common_bbox[1] = np.min(bboxs, axis=0)[1]
	common_bbox[2] = np.max(bboxs, axis=0)[2]
	common_bbox[3] = np.max(bboxs, axis=0)[3]
	imgs_cropped = []
	for img in imgs:
		img = img.crop(common_bbox)
		imgs_cropped.append(img)
	return imgs_cropped

if __name__ == "__main__":
	if VIDEO_MODE:
		''' Create gif from videos '''
		file_names = os.listdir(SOURCE_FOLDER)
		for file_name in file_names:
			if file_name.endswith(('.mp4','.mov','.avi','.webm')):
				file_path = os.path.join(SOURCE_FOLDER, file_name)
				video = VideoFileClip(file_path)
				# video = video.subclip((1,00.00),(1,30.00)) # trim the video by start time and end time
				# video = video.resize(0.5) # resize the video
				# video = video.speedx(1.5) # change the speed of the video
				video.write_gif(os.path.join(SOURCE_FOLDER, file_name.split('.')[0]+".gif"), fps=15)
	else:
		''' Create gif from a set of images '''
		images = []
		file_names = os.listdir(SOURCE_FOLDER)
		file_names.sort()
		for file_name in file_names:
			if file_name.endswith(('.png','.jpg','.jpeg')):
				file_path = os.path.join(SOURCE_FOLDER, file_name)
				image = Image.open(file_path)
				''' Keep transparency '''
				if image.mode == 'RGBA':
					alpha = image.getchannel('A')
					# Convert the image into P mode but only use 255 colors in the palette out of 256
					image = image.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
					# Set all pixel values below 128 to 255 , and the rest to 0
					mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
					# Paste the color of index 255 and use alpha as a mask
					image.paste(255, mask)
					# The transparency index is 255
					image.info['transparency'] = 255
				images.append(image)
		if TRIM_GROUP_MODE:
			images = trim_group(images)
		images[0].save(os.path.join(SOURCE_FOLDER, file_names[0].split('.')[0]+".gif"), save_all=True, append_images=images[1:], duration=300, loop=0, disposal=2)
