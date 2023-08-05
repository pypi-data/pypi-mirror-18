***********
GPSPhoto.py
***********

Module that uses ExifRead to extract GPS Tag Data from photos that have it.  Must have ExifRead module installed.  Functions will return empty dictionaries if photos do not contain GPS Tags.

This program is a work in progress, I do not have access to the way different devices store thier Exif GPS Data.  If the program doesn't work correctly and the output of the command line with the "-D" option gives results.  Please email me and I will will try to fix it.

This module was made possible by the ExifRead module.

Installation
************

PyPI
====
The recommended process is to install the `PyPI package <https://pypi.python.org/pypi/GPSPhoto>`_,
as it allows easily staying up to date::

    $ pip install gpsphoto

See the `pip documentation <https://pip.pypa.io/en/latest/user_guide.html>`_ for more info.


Compatibility
*************

GPSPhoto.py is tested on the following Python versions:

- 2.7
- 3.4

Usage
*****

Command Line
============

Some examples::

    $ python gpsphoto.py /path/to/image.jpg

    # For debugging information if you need to email me a to fix
    # a bug, please attach the output of the following

    $ python gpsphoto.py -D /path/to/image.jpg

    Sample Debug Output:

        GPS GPSTimeStamp: [16, 12, 28]
        Image GPSInfo: 504
        GPS GPSLongitude: [106, 34, 585371/10000]
        GPS GPSDate: 2016:10:01
        GPS GPSLatitudeRef: N
        GPS GPSLatitude: [35, 3, 95521/5000]
        GPS GPSProcessingMethod: ASCII
        GPS GPSLongitudeRef: W
        GPS GPSAltitudeRef: 0
        GPS GPSAltitude: 1636


Python Script
=============
::

    import gpsphoto
    # Get the data from image file and return a dictionary
    data = gpsphoto.getGPSData('/path/to/image.jpg')   
    rawData = gpsphoto.getRawData('/path/to/image.jpg')

    # Print out just GPS Data of interest
    for tag in data.keys():
        print "%s: %s" % (tag, data[tag])

    # Print out raw GPS Data for debugging
    for tag in rawData.keys():
        print "%s: %s" % (tag, rawData[tag])

Function Definitions
====================
::

    coord2decimal(parameter 1, parameter 2)

		  Function converts degrees, minutes and seconds to decimal. Returns a float.

		    This Function has two parameters
		    - parameter 1 is an argument of a list of floating point numbers.
		      this list either has 2 or 3 elements.  
		      An example of the list with 2 element is: 
		        [45.0, 45.1234] 
		      the first element is degrees the second element is minutes.
		      An example of the list with 3 elements is
		        [45.0, 44.0, 55.1234]
		      the first element is degrees the second element is minutes and
		      the third element is minutes.
		    - parameter 2 is a string of one of the following:
		        'N', 'S', 'E', 'W'
		      indicating what part of the world, for either Latitude or Longitude.

		decimal2Degree(parameter)
	
			Converts decimal coordinates to degrees, minutes, seconds and determines the quadrant

				Function takes one parameter a tuple or list of two elements containing floats.

    getGPSData(parameter)

    	Function returns a dictionary of GPS Data, with the following keys: 'Latitude', 'Longitude', 'UTC-Time', 'Date', 'Altitude'

      	Function takes one parameter, a string argument of a path to filename of an image.

    getRawData(parameter)

    	Function returns a dictionary of GPS ExifTags extracted by ExifRead.

      	Function takes one parameter, a string argument of a path to filename of an image.

		stripData(parameter 1, parameter 2)
	
			Function that takes a JPEG Image and strips the GPS Exif Data and saves a new image without the Exif data.

				Function takes two parameters one a string of the filename of the image to strip, the second parameter a string of the new file name.

		modGPSData(parameter 1, parameter 2, parameter 3, parameter 4)

			Function that takes a JPEG Image and modifies the Latitude, Longitude and Altitude of the Image.

				Function takes three required parameters and one optional parameter.
					- parameter 1 is a tuple or list of coordinates containing floats between -180 and 180.
					- parameter 2 is a string of the filename for the image to modify
					- parameter 3 is a string of the new filename for the image to save
					- parameter 4 is optional parameter of integer for the altitude in meters 

