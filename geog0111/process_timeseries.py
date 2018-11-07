# Some imports that might be useful...
# Put them at the top so they're easy to find
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from pathlib import Path
import gdal
from datetime import datetime, timedelta

def get_sfc_qc(qa_data, mask57 = 0b11100000):
    sfc_qa = np.right_shift(np.bitwise_and(qa_data, mask57), 5)
    return sfc_qa

def get_scaling(sfc_qa, golden_ratio=0.61803398875):
    weight = np.zeros_like(sfc_qa, dtype=np.float)
    for qa_val in [0, 1, 2, 3]:
        weight[sfc_qa == qa_val] = np.power(golden_ratio, float(qa_val))
    return weight


def find_mcdfiles(year, doy, tiles, folder, product='MCD15A3H'):
    data_folder = Path(folder)
    # Find all MCD files
    mcd_files = []
    for tile in tiles:
        sel_files = data_folder.glob(
            f"{product}.A{year:d}{doy:03d}.{tile:s}.*hdf")
        for fich in sel_files:
            mcd_files.append(fich)
    return mcd_files


def create_gdal_friendly_names(filenames, layer, product='MCD15A3H'):

    if product == 'MCD15A3H':
        grid = 'MOD_Grid_MCD15A3H'
    else:
        grid = product

    # Create GDAL friendly-names...
    gdal_filenames = []
    for file_name in filenames:
        fname = f'HDF4_EOS:EOS_GRID:'+\
                    f'"{file_name.as_posix()}":'+\
                    f'{grid}:{layer:s}'

        gdal_filenames.append(fname)
    return gdal_filenames



def mosaic_and_clip(tiles,
                    doy,
                    year,
                    ofolder=None,
                    folder="data/",
                    layer="Lai_500m",
                    shpfile="data/TM_WORLD_BORDERS-0.3.shp",
                    country_code="LU",
                    product='MCD15A3H',
                    frmat="MEM"):
    """
    #TODO docstring missing!!!!
    """

    if ofolder == None:
        ofolder = folder
    folder_path = Path(folder)
    ofolder_path = Path(ofolder)
    if not ofolder_path.exists():
        ofolder_path.mkdir()

    # Find all files to mosaic together
    hdf_files = find_mcdfiles(year, doy, tiles, folder,product=product)

    # Create GDAL friendly-names...
    gdal_filenames = create_gdal_friendly_names(hdf_files, layer, product=product)
    if frmat == "MEM":
        g = gdal.Warp(
            "",
            gdal_filenames,
            format="MEM",
            dstNodata=255,
            cutlineDSName=shpfile,
            cutlineWhere=f"FIPS='{country_code:s}'",
            cropToCutline=True)
        if g:
            data = g.ReadAsArray()
            return data
        else:
            print(f'failed to warp {str(gdal_filenames)} {year}, {doy}, {tiles}, {folder}')
    elif frmat == "VRT":

        try:
          geotiff_fnamex = f"{layer:s}_{year:d}_{doy:03d}_{country_code:s}.vrt"
          geotiff_fname  = ofolder_path/geotiff_fnamex
          g = gdal.Warp(
            geotiff_fname.as_posix(),
            gdal_filenames,
            format=frmat,
            dstNodata=255,
            cutlineDSName=shpfile,
            cutlineWhere=f"FIPS='{country_code:s}'",
            cropToCutline=True)
        except:
          pass
        if g:
            del g
            return geotiff_fname.as_posix()

    elif frmat == "GTiff":
        try:
          geotiff_fnamex = f"{layer:s}_{year:d}_{doy:03d}_{country_code:s}.tif"
          geotiff_fname  = ofolder_path/geotiff_fnamex
          g = gdal.Warp(
            geotiff_fname.as_posix(),
            gdal_filenames,
            format=frmat,
            dstNodata=255,
            cutlineDSName=shpfile,
            cutlineWhere=f"FIPS='{country_code:s}'",
            cropToCutline=True)
        except:
          pass
        if g:
            del g
            return geotiff_fname.as_posix()
        else:
            print(f'failed to warp {str(gdal_filenames)}  {year}, {doy}, {tiles}, {folder}')
    else:
        print("Only MEM, VRT or GTiff formats supported!")
        
        
def process_single_date(tiles,
                    doy,
                    year,
                    ofolder=None,
                    folder="data/",
                    shpfile="data/TM_WORLD_BORDERS-0.3.shp",
                    country_code="LU",
                    frmat="MEM"):
   
    try: 
      lai_data = mosaic_and_clip(tiles,
                    doy,
                    year,
                    ofolder=ofolder,
                    folder=folder,
                    layer="Lai_500m",
                    shpfile=shpfile,
                    country_code=country_code,
                    frmat="MEM")
      if lai_data is not None:
          lai_data = lai_data * 0.1
      # Note the scaling!
      else:
          return None,None 
      qa_data = mosaic_and_clip(tiles,
                    doy,
                    year,
                    ofolder=ofolder,
                    folder=folder,
                    layer="FparLai_QC",
                    shpfile=shpfile,
                    country_code=country_code,
                    frmat="MEM")
      sfc_qa = get_sfc_qc(qa_data)
    
      weights = get_scaling(sfc_qa)
      return lai_data, weights
    except:
      return None,None

from datetime import datetime, timedelta


def process_timeseries(year,
                       tiles,
                       ofolder=None,
                       folder="data/",
                       shpfile='data/TM_WORLD_BORDERS-0.3.shp',
                       country_code='LU',
                       frmat="MEM",
                       verbose=True):

    today = datetime(year, 1, 1)
    dates = []
    lai_array = None
    for i in range(92):
        if (i%10 == 0) and verbose:
            print(f"Looking for match to sample  {str(today):s}")
        if today.year != year:
            break
        doy = int(today.strftime("%j"))

        if frmat=="MEM":
          try:
            this_lai, this_weight = process_single_date(
              tiles,
              doy,
              year,
              ofolder=ofolder,
              folder=folder,
              shpfile=shpfile,
              country_code=country_code,
              frmat=frmat)
            if this_lai is not None:
              if verbose == 2: print(doy,np.median(this_lai[this_lai<25.5])) 
              if lai_array is None:
                # First day, create outputs!
                ny, nx = this_lai.shape
                lai_array = np.zeros((ny, nx, 92))
                weights_array = np.zeros((ny, nx, 92))
              lai_array[:, :, i] = this_lai
              weights_array[:, :, i] = this_weight
          except:
            pass
        dates.append(today)
        today = today + timedelta(days=4)
    return dates, lai_array, weights_array

