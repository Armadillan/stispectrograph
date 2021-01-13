#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Functions for data file i/o.
"""
import csv

def to_csv(dictionary, filename=None, headers=None, nm=False):
    """
    Save spectral data as csv.

    Parameters
    ----------
    dictionary : dict
        The dictrionary containing spectral data.
        Get using Image.get_spectral_data()
        The epected unit for wavelength is Angstrom.
    filename : str, optional
        The name of the file to save data to.
        If omitted, returns the csv file as a string.
    headers : iterable, optional
        The headers to put on top of the csv.
        Default is ("Wavelength ({unit})", "Intensity"),
        whwere {unit} is nm or A, depending on the nm parameter.
    nm : bool, optional
        Whether to convert Anstrom to nanometers. The default is False.

    Returns
    -------
    0 if saved to file.
    csv-formatted string if filename is omitted.

    """

    # Handle headers
    if headers and (isinstance(headers[0], str) and isinstance(headers[1], str)):
        try:
            headers = list(headers)
        except TypeError:
            headers = None
    else:
        headers = None

    # Set default headers if headers are not specified or invalid
    if headers is None:
        if nm:
            headers = ["Wavelength (nm)", "Intensity"]
        else:
            headers = ["Wavelength (A)", "Intensity"]

    if filename:
        # Remove .csv suffix if it exists
        # It's added later
        # So we don't get filename.csv.csv
        if filename[-4:].lower() == ".csv":
            filename=filename[:-4]

        with open(filename + ".csv", "w") as file:
            file.write(f"{headers[0]},{headers[1]}\n")
            for key, value in dictionary.items():
                if nm:
                    key /= 10
                file.write(f"{key},{value}\n")
    else:
        out = ""
        out += f"{headers[0]},{headers[1]}\n"
        for key, value in dictionary.items():
            if nm:
                key /= 10
            out += f"{key},{value}\n"
        return out
    return 0

def from_csv(csv_in):
    """
    Creates dictionary from csv file.
    Will ignore any columns beyond the first two.

    Can be called as

    >>> from_csv(filename)

    or

    >>> with open(filename) as file:
    ...    from_csv(file)

    Parameters
    ----------
    csv_in : str or file-like object
        Either a filename to open, or an file-like object to
        get data from.


    Returns
    -------
    headers : list or NoneType
        The top row in the csv file. If the top row is numeric, instead
        includes it in the data and returns None.
    dict
        Dictionary of spectral data from the csv file.

    """

    if isinstance(csv_in, str):
        file = open(csv_in)
        reader = csv.reader(file)
    else:
        reader = csv.reader(csv_in)

    reader = list(reader)

    if not (reader[0][0].isnumeric() and reader[0][1].isnumeric()):
        headers = reader.pop(0)
    else:
        headers = None

    try:
        file.close()
    except (NameError, AttributeError):
        pass

    return (headers, {float(row[0]):float(row[1]) for row in reader})

def from_csv_string(string):
    reader = csv.reader(string)

    if not (reader[0][0].isnumeric() and reader[0][1].isnumeric()):
        headers = reader.pop(0)
    else:
        headers = None

    return (headers, {row[0]:row[1] for row in reader})