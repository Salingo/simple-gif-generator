# simple-gif-generator

A python script for gif generation.

## Instructions
Make sure you have installed Pillow (to generate from images) and moviepy (to generate from videos):

`pip install Pillow moviepy`

To convert videos to gifs, put all videos in a source folder, the script will generate gif for each video. You can customize the fps, speed, resolution, start/end time in the code.

To convert image frames to gif, put all images in a source folder, the script will generate gif follow the order of the file names.
Additionally, this script can trim the redundant background of the images in source folder (by the minimum boundary of the images). Set `TRIM_GROUP_MODE` to `True` to enable this feature.

## Usage

`python gif.py <source_folder> <0 or 1>`, 0 for image mode, 1 for video mode.
