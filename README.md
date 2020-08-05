# simple-gif-generator

A python script for gif generation.

Make sure you have installed Pillow: `pip install Pillow`

Put all frames in a folder, the script will generate the gif follow the order of the file names.

Additionally, this script can help trim the redundant boundary of the images. Set `TRIM_SET` to `True` to enable this feature.

Use example: `python gif.py ./my_images ./output.gif`
