
# stispectrograph
![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)

This is a python package and script meant to replace part (maybe eventually all) of the functionality of
SBIG's "ST-i Spectroscopy Program" used with the ST-i spectrograph.

This package defaults to Angstrom for wavelength, like the original software.

## Installation
`pip install stispectrograph`

Or clone github repo and install from source:  
`python setup.py install`

## Functionality

The included script `fits_to_csv.py` can be used as a command line tool to extract spectral data from fits files to csv, similar to the "Save Spectral Data as Text File" function in the original software.

I recommend taking exposures using SBIG's CCDops software, using the procedure given in the spectrograph manual.
This software will only accept images with dimensions 121x648 pixels, which in
CCDops means setting resolution to 1xN and vertical binning to 4.

Usage: `fits_to_csv mercury_line_pixel [path] [nm]`

The csv files are created in the same directory as the images, with the same names.
The x-value at which the 5461 A mercury line appears in the image must be provided.
If a path to a directory is specified, extracts data from all FITS files in that directory.
If a filename is specified instead, extracts data from that file only.
Omitting a path extracts data from all files in the current working directory.
If the argument "nm" is provided, outputs wavelength in nm instead of A.

The pixel value at which the 5461 A mercury line appears in the image depends on the calibration process.
Consult the spectrograph manual for how to identify this line.

Examples:  
`fits_to_csv 337 image.FIT` Extracts data from `image.FIT` and creates `image.csv` in the same directory.  
`fits_to_csv 337 Astronomy\images` Extracts data from all fits files in `Astronomy\images`, creating separate csv files for each in that directory.  
`fits_to_csv 337 "C:\Documents\Astronomy\Spectrograph images\image.fit" nm` Extracts data from `image.fit`, with the wavelength in nanometers.  
`fits_to_csv 337 nm` Extracts data from all fits files in the current working directory, with the wavelength in nanometers.

For more advanced use cases, such as getting binned data, cropping to a
specific part of the image (the defualt crop is like the original software's,
pixel 55 to 65) or getting the data in a different format, the python package can be used to build other tools. I'm working on better documentation, for now the comments in the code will have to suffice.

The current implementation has:
* The class `stispectrograph.image.Image`, for extracting data from spectrograph images in fits format.
* The module `stispectrograph.io` with functions for saving data to csv, and getting data from csv and csv-formatted strings.
  * `stispectrograph.io.to_csv`
  * `stispectrograph.io.from_csv`
  * `stispectrograph.io.from_csv_string`
 * The module `stispectrograph.visualisation` which can currently create a nice colored graph of data. Work is in progress to create functionality similar to the original software.
 * A dictionary relating horizontal pixels (relative to the 5461 A Mercury line) to the corresponding wavelengths (`stispectrograph.constants.WAVELENGTH_PER_PIXEL`).

## TODOs
* Create better documentation for the stispectrograph package.
* Create a visualisation of the spectrum, like the original software.
* Create additional scripts, or a more universal tool.

This software is published under the MIT License, see LICENSE.txt.
