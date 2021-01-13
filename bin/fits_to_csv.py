#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script for extracting spectral data from fits files to csv.

Usage: fits_to_csv mercury_line_pixel [path] [nm]

The csv files are created in the same directory as the images, with the same names.
The x-value at which the 5461 A mercury line appears in the image must be provided.
If a path to a directory is specified, extracts data from all FITS files in that directory.
If a filename is specified instead, extracts data from that file only.
Omitting a path extracts data from all files in the current working directory.
If the argument "nm" is provided, outputs wavelength in nm instead of A.
"""

import sys
import os
import re

from stispectrograph.image import Image
from stispectrograph.io import to_csv

fits_regex = re.compile(r"(.+)\.(FIT|fit)")

if len(sys.argv) in (2,3,4):
    cwd = False
    nm = False
    headers=["Wavelength (A)", "Intensity"]

    if len(sys.argv) == 2:
        path = os.getcwd()
        cwd = True
    else:
        path_and_nm = sys.argv[2:]
        for i in range(len(path_and_nm)):
            if path_and_nm[i].lower() in ("nm", "true", "nm=true"):
                del path_and_nm[i]
                nm= True
                headers=["Wavelength (nm)", "Intensity"]
            elif path_and_nm[i].lower() in ("false", "nm=false"):
                del path_and_nm[i]
        try:
            path = path_and_nm[0]
        except IndexError:
            path = os.getcwd()
            cwd = True

    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)

    try:
        mercury_line = int(sys.argv[1])
    except ValueError:
        print(f"\nError: Invalid mercury line pixel value: \"{sys.argv[1]}\"\n")
        sys.exit(2)

    if not os.path.exists(path):
        print(f"\nError: The path\"{path}\" does not exits.\n")
        sys.exit(2)

    if os.path.isfile(path):
        if (match := fits_regex.match(path)):

            try:
                image = Image(path)
            except Image.InvalidImageShapeError as e:
                print(f"\nError: File \"{path}\" has incorrect dimensions:")
                print(str(e)+"\n")
                sys.exit(1)

            data = image.get_spectral_data(mercury_line)
            to_csv(
                data,
                filename=os.path.join(os.path.dirname(path),match.group(1)),
                headers=headers,
                nm=nm
                )
            print("Saved " + match.group(1) + ".csv")

        else:
            print(f"\nError: \"{path}\" is not a FITS file.\n")
            sys.exit(2)

    else:
        found = False
        for file in os.listdir(path):
            if (match := fits_regex.match(file)):
                file = os.path.join(path, file)
                found = True
                try:
                    image = Image(file)
                except Image.InvalidImageShapeError as e:
                    if cwd:
                        name = os.path.basename(file)
                    else:
                        name = file
                    print( f"\nError: File \"{name}\" has incorrect dimensions:")
                    print(str(e)+"\n")
                    continue
                data = image.get_spectral_data(mercury_line)
                to_csv(
                    data,
                    os.path.join(path, match.group(1)),
                    headers=headers,
                    nm=nm
                    )
                print("Saved " + match.group(1) + ".csv")
        if not found:
            print(f"\nError: There are no FITS files in \"{path}\"\n")
            sys.exit(2)

    sys.exit(0)

elif len(sys.argv) == 1:
    print(
    f"""
    Usage: {os.path.basename(sys.argv[0])} mercury_line_pixel [path] [nm]
    Extracts spectral data from FITS files to csv.
    The csv files are created in the same directory as the images, with the same names.
    The x-value at which the 5461 A mercury line appears in the image must be provided.
    If a path to a directory is specified, extracts data from all FITS files in that directory.
    If a filename is specified instead, extracts data from that file only.
    Omitting a path extracts data from all files in the current working directory.
    If the argument "nm" is provided, outputs wavelength in nm instead of A.
"""
    )


else:
    print(f"\nError: Expected 1-3 arguments, got {len(sys.argv)-1}.")
