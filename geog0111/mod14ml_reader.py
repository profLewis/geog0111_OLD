from pathlib import Path

import gdal
import numpy as np


def get_mod14(folder="data/mod14_data"):
    data_dir = Path(folder)
    files = [f for f in data_dir.glob("MOD14CMH*hdf")]
    files = sorted(files)
    return files


def subsample_data(data, size=10, aggr=np.sum):
    """Subsample a 2D dataset by aggregating. Assumes that the input
    image or dataset will be aggregated over chunks of `size`
    by `size` pixels."""
    m, n = data.shape
    mm, nn = int(m/size), int(n/size)
    output = np.zeros((mm, nn))
    for i in range(mm):
        for j in range(nn):
            x = aggr(data[(size*i):(size*(i+1)), (size*j):(size*(j+1))])
            output[i,j] = x
    return output


def read_mod14_data(fich):
    fich = Path(fich)
    data = gdal.Open('HDF4_SDS:UNKNOWN:"%s":1' % str(fich)).ReadAsArray()
    return subsample_data(data)

def create_data_dictionary():
    dates = zip((int(f.name.split(".")[1][:4]) for f in get_mod14()),
                (int(f.name.split(".")[1][4:]) for f in get_mod14()))

    dataset = (read_mod14_data(f) for f in get_mod14())

    mod14_data = dict(zip(dates, dataset))
    return mod14_data