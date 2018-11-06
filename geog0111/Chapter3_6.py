
import sys
year = 2017
if len(sys.argv) == 3:
    country_code = sys.argv[1]
    year = int(sys.argv[2])
elif len(sys.argv) == 2:
    country_code = sys.argv[1]
else:
    country_code = 'UK'

force = False
save = True
download = True

print(country_code,year)

import numpy as np
import sys
import os
from pathlib import Path
import gdal
from datetime import datetime, timedelta

shpfile = "data/TM_WORLD_BORDERS-0.3.shp"

tiles = []
for h in [17, 18]:
    for v in [3, 4]:
        tiles.append(f'h{h:02d}v{v:02d}')

        
fname = f'lai_data_{year}_{country_code}.npz'
ofile = Path('data')/fname
try:
    # read data from npz file
    lai = np.load(ofile)
except:
    print(f"{ofile} doesn't exist: sort the pre-requisites")

from osgeo import gdal, gdalconst,osr
import numpy as np
from geog0111.process_timeseries import mosaic_and_clip

# set to True if you want to override
# the MODIS projection (see above)
use_6974 = False

'''
https://stackoverflow.com/questions/10454316/
how-to-project-and-resample-a-grid-to-match-another-grid-with-gdal-python
'''
        
# first get an exemplar LAI file, clipped to
# the required limits. We will use this to match  
# the t2 dataset to
match_filename = mosaic_and_clip(tiles,1,year,ofolder='tmp',\
                    country_code=country_code,shpfile=shpfile,frmat='GTiff')

print(match_filename)

'''
Now get the projection, geotransform and dataset
size that we want to match to
'''
match_ds = gdal.Open(match_filename, gdalconst.GA_ReadOnly)
match_proj = match_ds.GetProjection()
match_geotrans = match_ds.GetGeoTransform()
wide = match_ds.RasterXSize
high = match_ds.RasterYSize

print('\nProjection from file:')
print(match_proj,'\n')

'''
set Projection 6974 from SR-OR
by setting use_6974 = True
'''
if use_6974:
    print('\nProjection 6974 from SR-ORG:')
    modis_wkt = 'data/modis_6974.wkt'
    match_proj = open(modis_wkt,'r').readline()
    match_ds.SetProjection(match_proj)
    print(match_proj,'\n')

'''
Visualise
'''
# close the file -- we dont need it any more
del match_ds

from osgeo import gdal, gdalconst,osr
import numpy as np

# set up conditions
src_filename = f'data/europe_data_{year}.nc'
'''
access information from source
'''
src_dataname = 'NETCDF:"'+src_filename+'":t2m'
src     = gdal.Open(src_filename, gdalconst.GA_ReadOnly)

'''
Get geotrans, data type and number of bands
from source dataset
'''
band1 = src.GetRasterBand(1)
src_proj = src.GetProjection()
src_geotrans = src.GetGeoTransform()
nbands = src.RasterCount
src_format = band1.DataType
nx = band1.XSize
ny = band1.YSize

print('Information found')
print('GeoTransform:   ',src_geotrans)
print('Projection:     ',src_proj)
print('number of bands:',nbands)
print('format:         ',src_format)
print('nx,ny:          ',nx,ny)

# read data
t2m = band1.ReadAsArray()

dst = gdal.GetDriverByName('MEM').Create('', wide, high, nbands, src_format)

dst.SetGeoTransform( match_geotrans )
dst.SetProjection( match_proj)

print('Information found')
print('wide:      ',wide)
print('high:      ',high)
print('geotrans:  ',match_geotrans)
print('projection:',match_proj)

# Do the work: reproject the dataset
# This will take a few minutes, depending on dataset size
_ = gdal.ReprojectImage(src, dst, src_proj, match_proj, gdalconst.GRA_Bilinear)


xOrigin = match_geotrans[0]
yOrigin = match_geotrans[3]
pixelWidth = match_geotrans[1]
pixelHeight = match_geotrans[5]

extent = (xOrigin,xOrigin+pixelWidth*wide,\
         yOrigin+pixelHeight*(high),yOrigin+pixelHeight)

print(extent)

t2m = dst.GetRasterBand(1).ReadAsArray()
match_ds = gdal.Open(match_filename, gdalconst.GA_ReadOnly).ReadAsArray()

dst_filename = src_filename.replace('.nc',f'_{country_code}.tif')
frmat = 'GTiff'
if (not Path(dst_filename).exists()) or force:
    g = gdal.Warp(dst_filename,
            dst,
            format=frmat,
            dstNodata=-300,
            cutlineDSName=shpfile,
            cutlineWhere=f"FIPS='{country_code:s}'",
            cropToCutline=True)
    del g

del dst # Flush

print(dst_filename)
t2m = gdal.Open(dst_filename, gdalconst.GA_ReadOnly)
t2m = t2m.GetRasterBand(1).ReadAsArray()
t2m[t2m==-300] = np.nan
match_ds = gdal.Open(match_filename, gdalconst.GA_ReadOnly).ReadAsArray()

meta = gdal.Open(src_filename).GetMetadata()

print(meta['time#units'])
timer = meta['NETCDF_DIM_time_VALUES']
print(timer[:100])

# split the string into integers
timer = [int(i) for i in meta['NETCDF_DIM_time_VALUES'][1:-1].split(',')]

print (timer[:20])
# split the string into integers
# convert to days
timer = [float(i)/24. for i in meta['NETCDF_DIM_time_VALUES'][1:-1].split(',')]

print (timer[:20])
from datetime import datetime,timedelta

# add base date
# split the string into integers
# convert to days
timer = [(datetime(1900,1,1) + timedelta(days=float(i)/24.)) \
         for i in meta['NETCDF_DIM_time_VALUES'][1:-1].split(',')]

print (timer[:20])
from osgeo import gdal, gdalconst,osr
import numpy as np
from geog0111.process_timeseries import mosaic_and_clip
from datetime import datetime 

from osgeo import gdal, gdalconst,osr
import numpy as np
from geog0111.process_timeseries import mosaic_and_clip
from datetime import datetime,timedelta
from geog0111.match_netcdf_to_data import match_netcdf_to_data
from geog0111.geog_data import procure_dataset
from pathlib import Path

# set conditions

shpfile = "data/TM_WORLD_BORDERS-0.3.shp"
src_filename = f'data/europe_data_{year}.nc'
dst_filename = f'data/europe_data_{year}_{country_code}.tif'
t2_filename = f'data/europe_data_{year}_{country_code}.npz'
# read in the LAI data for given country code
tiles = []
for h in [17, 18]:
    for v in [3, 4]:
        tiles.append(f"h{h:02d}v{v:02d}")
        

#read LAI
fname = f'lai_data_{year}_{country_code}.npz'
ofile = Path('data')/fname
lai = np.load(ofile)

if not Path(t2_filename).exists():
    print(f'calculating dataset match in {t2_filename}')
    # first get an exemplar LAI file, clipped to
    # the required limits. We will use this to match  
    # the t2 dataset to
    match_filename = mosaic_and_clip(tiles,1,year,\
                        country_code=country_code,\
                        shpfile=shpfile,frmat='GTiff')
    '''
    Match the datasets using the function
    we have developed
    '''
    meta = gdal.Open(src_filename, gdalconst.GA_ReadOnly).GetMetadata()

    timer,dst_filename,extent = match_netcdf_to_data(\
                                    src_filename,match_filename,\
                                    dst_filename,year,\
                                    country_code=country_code,\
                                    shpfile=shpfile,\
                                    nodata=-300,frmat='GTiff',\
                                    verbose=True)

    # read and interpret the t2 data and flip
    temp2 = gdal.Open(dst_filename).ReadAsArray()[:,::-1]
    temp2[temp2==-300] = np.nan
    temp2 -= 273.15
    # save these
    print(f'saving data to {t2_filename}')
    np.savez_compressed(t2_filename,timer=timer,temp2=temp2,extent=extent)

else:
    print(f'dataset in {t2_filename} exists')
    
print('done')
t2data = np.load(t2_filename)
timer,temp2,extent = t2data['timer'],t2data['temp2'],t2data['extent']

import scipy
import scipy.ndimage.filters

# want sigma as low as we can deal with, whilst 
# still interpolating effectively
sigma = 3

# read in the LAI data for given country code
fname = f'lai_data_{year}_{country_code}.npz'
ofile = Path('data')/fname

# read data from npz file
lai = np.load(ofile)

# set up filter
x = np.arange(-3*sigma,3*sigma+1)
gaussian = np.exp((-(x/sigma)**2)/2.0)

FIPS = country_code
dates, lai_array, weights_array = lai['dates'],lai['lai'],lai['weights']
print(lai_array.shape, weights_array.shape) #Check the output array shapes

from geog0111.geog_data import procure_dataset
import numpy as np
from pathlib import Path

'''
LAI data
'''
# read in the LAI data for given country code
lai_filename = f'data/lai_data_{year}_{country_code}.npz'
# get the dataset in case its not here
procure_dataset(Path(lai_filename).name,verbose=False)

lai = np.load(lai_filename)
print(lai_filename,list(lai.keys()))

'''
T 2m data
'''
t2_filename = f'data/europe_data_{year}_{country_code}.npz'
# get the dataset in case its not here
procure_dataset(Path(t2_filename).name,verbose=False)
t2data = np.load(t2_filename)
print(t2_filename,list(t2data.keys()))
