#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class for handling spectrograph images.
"""

from astropy.io import fits

class Image:
    """
    Class for extracting data from a FITS image.
    Opens a file and extracts its data, which is held in the Image object.
    """
    from stispectrograph.constants import WAVELENGTH_PER_PIXEL

    class InvalidImageShapeError(IOError):
        """
        Error for when the image has the wrong dimensions.
        """
        def __init__(self, shape):
            self.shape = shape

        def __str__(self):
            return f"Image has dimensions {self.shape[0]}x{self.shape[1]} pixels, expected 121x648 pixels."

    def __init__(self, file):
        """
        Opens the file and gets its data, which is held in the
        Image object.
        """

        self.__HDUlist = fits.open(file)
        self.__HDU = self.__HDUlist[0].copy()
        self.__HDUlist.close()

        self.__data = self.__HDU.data.copy()
        if self.__data.shape != (121,648):
            raise self.InvalidImageShapeError(self.__data.shape)

    @property
    def data(self):
        """
        Gets the actual image data as a 2-dimensional numpy array
        with a value for each pixel.

        Returns
        -------
        numpy.ndarray
            The image as an array of pixel values.

        """
        return self.__data

    def cropped_data(self, upper, lower):
        """
        Gets the image data, but cropped vertically.

        Parameters
        ----------
        upper : int
            The upper pixel number to start the crop from.
            Should be smaller than lower.
        lower : int
            The lower pixel at which to end the crop.
            Should be greater than upper.

        Returns
        -------
        numpy.ndarray
            The cropped image as an array of pixel values..

        """
        # Numpy arrays start at 0, pixel numbering starts at 1
        # So pixel n is index n-1 in the numpy array
        return self.data[upper-1:lower]

    def get_spectral_data(self, mercury_line, binned=0, upper_crop=55, lower_crop=65):
        """
        Gets the intensity for each wavelength present in the image,
        either individually for every pixel or binned in set intervals.

        Parameters
        ----------
        mercury_line : int
            The pixel x-value at which the 5461 Å mercury line appears
            in the image.
        binned : int, optional
            The increments in which to bin the data. If this parameter
            is less than 10, returns intensity per pixel column
            (for every individual wavelength in the image). The default is 0.
        upper_crop : int, optional
            The upper pixel y-value from which to crop the image before
            extracting data. Should be smaller than lower_crop.
            The default is 55.
        lower_crop : TYPE, optional
            The lower pixel y-value to which to crop the image before
            extracting data. Should be greater than upper_crop.
            The default is 65.

        Returns
        -------
        dict
            A dictionary relating wavelengths to intensities.
            {wavelength: intensity}

        """
        pixel_per_wavelength = {}
        for key, value in self.WAVELENGTH_PER_PIXEL.items():
            # Swaps the wavelengths and pixels, and sets 0 to mercury line, so
            # That the correct pixel is mapped to the correct wavelength for this
            # particular image.
            # Also strips all pixels not present in image
            # (smaller than 1 and larger than 648)
            if 1 <= (pixel := key + mercury_line) <= 648:
                pixel_per_wavelength[value] = pixel

        # Cropped data to extract wavelength intensities from
        data = self.cropped_data(upper_crop, lower_crop)



        def column_average(column):
            """
            Takes the average of all pixels with specified x-value
            between lower_crop and upper_crop, then subtracts 100
            from it, like the original software.
            """
            column_height = lower_crop - upper_crop + 1
            column_sum = 0

            for row in range(column_height):
                column_sum += data[row][column]
            # Subtracts 100, because that is what
            # the original software does:
            return column_sum / column_height - 100


        if (not binned) or (binned <= 10):
            out = {}

            for wavelength, pixel in pixel_per_wavelength.items():
                # Numpy arrays start at 0! So subtract 1 from pixel value
                out[wavelength] = column_average(pixel-1)

        else:
            low = 4000
            high = 11000
            not_binned = self.get_spectral_data(
                mercury_line=mercury_line, upper_crop=upper_crop,
                lower_crop=lower_crop)
            out = {}
            for lower in range(low, high+binned, binned):
                binned_value = 0
                for key, value in not_binned.items():
                    if lower <= key < lower + binned:
                        binned_value += value
                out[lower] = binned_value

        return out
