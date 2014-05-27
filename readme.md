exifsort
========

Sort images into directories based on their exchangeable image file format

###Features###
 - Reads JPEG (JPG) and Canon Raw Format (CR2)
 - Parses EXIF written by Canon EOS series cameras
 - Sorts into directories based on the ordered list of sort parameters
 - Copy or Move images
 - Sort Parameters
 	- Date
 	- Camera Body
 	- Camera Lens
 	- Camera Orientation
 	- Flash Fire

###Simple Example###
This example is just using a single sort parameter for date:

	$ python exifsort.py --date ~/Downloads/60D

There are 4 photos in this folder, with the corresponding EXIF dates:

	~/Downloads/60D/DSC_0081.JPG, 2004:10:05 12:15:22
	~/Downloads/60D/IMG_0002.JPG, 2010:10:04 21:08:09
	~/Downloads/60D/IMG_0520.JPG, 2010:12:26 11:26:36
	~/Downloads/60D/IMG_1131.JPG, 2010:12:26 14:81:18

This should result in the creation of 3 folders within the 60D folder

	~/Downloads/60D/2004.10.05 (DSC_0081.JPG)
	~/Downloads/60D/2010.10.04 (IMG_0002.JPG)
	~/Downloads/60D/2010.12.26 (IMG_0520.JPG, IMG_1131.JPG)

###Fancy Example###
This example chains several parameters:

	$ python exifsort.py --date --camera --orient ~/Downloads/60D

There are 4 photos in this folder, with the corresponding EXIF daters:

	~/Downloads/60D/DSC_0081.JPG, 2004:10:05 12:15:22, Nikon D70, Horizontal
	~/Downloads/60D/IMG_0002.JPG, 2010:10:04 21:08:09, Canon EOS 60D, Horizontal
	~/Downloads/60D/IMG_0520.JPG, 2010:12:26 11:26:36, Canon EOS 60D, Vertical
	~/Downloads/60D/IMG_1131.JPG, 2010:12:26 14:81:18, Canon EOS 60D, Horizontal

This should result in the creation of many folders/subdirs, Something that looks like this:

	~/Downloads/60D/2004.10.05/Nikon D70/Horizontal 	(DSC_0081.JPG)
	~/Downloads/60D/2010.10.04/Canon EOS 60D/Horizontal (IMG_0002.JPG)
	~/Downloads/60D/2010.12.26/Canon EOS 60D/Vertical	(IMG_0520.JPG)
	~/Downloads/60D/2010.12.26/Canon EOS 60D/Horizontal	(IMG_1131.JPG)


###Dependencies###
[exif-py](https://github.com/ianare/exif-py)

	virtualenv: pip install exifread

	Fedora: sudo yum install python-exif
	
	Ubuntu: sudo apt-get install python-exif
