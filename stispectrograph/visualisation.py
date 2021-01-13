#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors

def wavelength_to_rgb(wavelength, gamma=0.8):
    ''' Taken from http://www.noah.org/wiki/Wavelength_to_RGB_in_Python
    This converts a given wavelength of light to an
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    Additionally alpha value set to 0.5 outside range
    '''
    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 750:
        A = 1.
    else:
        A=0.5
    if wavelength < 380:
        wavelength = 380.
    if wavelength >750:
        wavelength = 750.
    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif wavelength >= 440 and wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif wavelength >= 645 and wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    return (R,G,B,A)


def graph(data, *args, **kwargs):
    """
    DATA EXEPECTED IN NM

    """
    #Maps wavelengths to values between 0 and 1 and creates a colormap
    clim=(350,780)
    norm = plt.Normalize(*clim)
    wl = np.linspace(clim[0], clim[1], 10000)
    colorlist = list(zip(norm(wl),[wavelength_to_rgb(w) for w in wl]))
    spectralmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        "spectrum", colorlist
        )

    # Splits data into two lists
    wavelengths = list(data.keys())
    intensity = list(data.values())

    fig, axs = plt.subplots(1, 1, figsize=(12,6), tight_layout=False)

    # Plots the line
    plt.plot(wavelengths, intensity, color='darkred', linewidth=2)

    #Makes meshgrid and finds size (extent) of image
    y = np.linspace(min(intensity), max(intensity), 100)
    X,Y = np.meshgrid(wavelengths, y)
    extent=(np.min(wavelengths), np.max(wavelengths), np.min(y), np.max(y))

    # Creates the imshow image on top of the plot
    plt.imshow(X, clim=clim,  extent=extent, cmap=spectralmap, aspect='auto')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity')

    # Makes the area above the line white.
    plt.fill_between(wavelengths, intensity, max(intensity)*1.05, color='w')

    plt.show()