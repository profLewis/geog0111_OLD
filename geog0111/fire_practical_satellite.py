#!/usr/bin/env python
"""Some functions to process MxD14 CMG files for the fire practical
"""

from pathlib import Path

import numpy as np

import gdal

from scipy.stats import mode


__author__ = "J Gomez-Dans"
__copyright__ = "Copyright 2018 J Gomez-Dans"
__version__ = "1.0 (03.12.2018)"
__email__ = "j.gomez-dans@ucl.ac.uk"


def get_mod14(folder="data/mod14_data", skip_files=2):
    """Gets hold of the MOD14 data. We can skip a couple of files
    from 2000, and just read in the data from 2001 to 2016.
    
    Parameters
    -----------
    folder: str
        The folder where the files are all located
    skip_files: int
        Number of files to skip at the start of the time series
    
    Returns
    -------
    REturns a list of pathlib objects with all the MOD14CMH HDF files
    """
    data_dir = Path(folder)
    files = [f for f in data_dir.glob("MOD14CMH*hdf")]
    files = sorted(files)
    return files[skip_files:]  # Skip 2000 as only two months


def subsample_data(data, size=10, aggr=np.sum):
    """Subsample a 2D dataset by aggregating. Assumes that the input
    image or dataset will be aggregated over chunks of `size`
    by `size` pixels. You can select what aggregation method you 
    want to use.
    
    Parameters
    -----------
    data: ndarray
        A 2D array of fire counts (for example)
    size: int
        The size of the aggregation in pixels. Identical for x and y
    aggr: function
        A function to perform the aggregation. By default, sum
    
    Returns
    ---------
    A downsampled and aggregated dataset
    """
    assert size >= 1, "size needs to be >= 1"
    m, n = data.shape
    mm, nn = int(m / size), int(n / size)
    output = np.zeros((mm, nn))
    for i in range(mm):
        for j in range(nn):
            x = aggr(data[(size * i) : (size * (i + 1)), (size * j) : (size * (j + 1))])
            output[i, j] = x
    return output


def read_mod14_data(fich, layer=1):
    """Read the MOD14 data. Uses first layer by default.
    
    Parameters
    -----------
    fich: str
        A MOD14 HDF file
    layer: int
       The layer in the HDF file.
       
    Result
    -------
    Returns the data. Pixels with values <0 are set to 0.
    """
    fich = Path(fich)
    if not fich.exists():
        raise IOError(f"{fich:s} does not appear to exist")
    data = gdal.Open('HDF4_SDS:UNKNOWN:"%s":%d' % (str(fich), layer)).ReadAsArray()
    data[data < 0] = 0
    return data


def create_subsampled_dataset():
    """Creates a subsampled datasets and extracts the dates.
    
    Returns
    --------
    Returns two arrays: a dates array (2 columns, years and months), as well
    as a 3D array of months*years, nx, ny cells.
    """
    dates = zip(
        (int(f.name.split(".")[1][:4]) for f in get_mod14()),
        (int(f.name.split(".")[1][4:]) for f in get_mod14()),
    )

    dataset = (subsample_data(read_mod14_data(f)) for f in get_mod14())

    return np.array(list(dates)), np.array(list(dataset))


def find_peak_and_fires(mod14_dates, mod14_data):
    """A function to find the peak fire month (in this case using the mode,
    but other criteria could be implemented) and monthly fire counts on that
    month for all years. Takes as inputs the dates 2D array and mod14 data
    that you get from calling the function `create_subsampled_dataset`.
    """

    n_months, nn, mm = mod14_data.shape
    n_years = int(n_months / 12)
    peak_fire_month_year = np.zeros((n_years, nn, mm))

    for year in range(n_years):
        for i in range(nn):
            for j in range(mm):
                this_year = mod14_data[(year * 12) : ((year + 1) * 12), i, j]
                if this_year.sum() == 0:
                    peak_fire_month_year[year, i, j] = -1
                else:
                    peak_fire_month_year[year, i, j] = np.argmax(this_year) + 1

    # Using the mode
    peak_fire_month = (mode(peak_fire_month_year, axis=0).mode[0]).astype(np.int)

    fire_count_year = np.zeros((n_years, nn, mm))

    for year in range(n_years):
        for i in range(nn):
            for j in range(mm):
                if peak_fire_month[i, j] >= 1:
                    fire_count_year[year, i, j] = mod14_data[
                        (year * 12) : ((year + 1) * 12), i, j
                    ][peak_fire_month[i, j] - 1]
    return peak_fire_month, fire_count_year
