import os
import sys
import numpy as np
from PIL import Image, ImageChops

IMG_FOLDER = sys.argv[1]
SAVE_PATH = sys.argv[2]
TRIM_SET = True

''' Trim all images in the IMG_FOLDER by the common minimum bbox '''
def trim_set(imgs):
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
	images = []
	file_names = os.listdir(IMG_FOLDER)
	file_names.sort()
	for file_name in file_names:
		if file_name.endswith(('.png','.jpg','.jpeg')):
			file_path = os.path.join(IMG_FOLDER, file_name)
			img = Image.open(file_path)
			''' Keep transparency '''
			if img.mode == 'RGBA':
				alpha = img.getchannel('A')
				# Convert the image into P mode but only use 255 colors in the palette out of 256
				img = img.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
				# Set all pixel values below 128 to 255 , and the rest to 0
				mask = Image.eval(alpha, lambda a: 255 if a <=128 else 0)
				# Paste the color of index 255 and use alpha as a mask
				img.paste(255, mask)
				# The transparency index is 255
				img.info['transparency'] = 255
			images.append(img)
	if TRIM_SET:
		images = trim_set(images)
	images[0].save(SAVE_PATH, save_all=True, append_images=images[1:], duration=100, loop=0)
