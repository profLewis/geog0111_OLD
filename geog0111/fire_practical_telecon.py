#!/usr/bin/env python
"""A function to downlaod process teleconnections data
"""
import urllib.request
from pathlib import Path

import numpy as np


__author__ = "J Gomez-Dans"
__copyright__ = "Copyright 2018 J Gomez-Dans"
__version__ = "1.0 (03.12.2018)"
__email__ = "j.gomez-dans@ucl.ac.uk"


def get_telecon_data(
    telecon="nina34.data",
    dest_folder="data/mod14_data/",
    base_url="https://www.esrl.noaa.gov/psd/data/correlation/",
    start_year=2000,
    end_year=2016,
):
    """Downloads and processes the telenconnection data for easy 
    model development. It returns a 2D array, where each row
    has 24 elements: element 12 is the teleconnection for January
    of the relevant year, and elements 0 to 11 are the teleconnection
    values for the months of the previous year.
    
    Parameters
    ------------
    telecon: str
        The name of the teleconnection. You can look it up from
        [this page](https://www.esrl.noaa.gov/psd/data/climateindices/list/)
    dest_folder: str
        The destination folder. It'll save the teleconnection there
    base_url: str
        The base URL for the NOAA server
    start_year: int
        The start year ;-)
    end_year: int
        The end year
    
    Returns
    ---------
    A 2D array with the teleconnection.
    """

    n_years = end_year - start_year
    url = base_url + telecon
    req = urllib.request.urlretrieve(url, filename=dest_folder + telecon)

    txt = open(dest_folder + telecon, "r").readlines()[1:-3]

    telecon = np.loadtxt(txt)
    passer = np.logical_and(telecon[:, 0] >= start_year, telecon[:, 0] <= end_year)

    telecon = telecon[passer, :][:, 1:]
    ext_telecon = np.zeros((telecon.shape[0], telecon.shape[1] * 2))
    for year in range(1, n_years + 1):
        ext_telecon[year, :12] = telecon[year - 1]
        ext_telecon[year, 12:] = telecon[year]

    ext_telecon = ext_telecon[1:, :]
    return ext_telecon
