import numpy as np
import sys
import os
from pathlib import Path
import gdal
from datetime import datetime, timedelta


# get the MODIS LAI dataset for 2016/2017 for W. Europe
from geog0111.geog_data import procure_dataset
from pathlib import Path
import sys
year = 2017
if len(sys.argv) == 3:
    country_code = sys.argv[1]
    year = int(sys.argv[2])
elif len(sys.argv) == 2:
    country_code = sys.argv[1]
else:
    country_code = 'UK'
verbose = True

print(sys.argv,year,country_code)

files = list(Path('data').glob('MCD15A3H.A201[6-7]*h1[7-8]v0[3-4].006*hdf'))
if len(files) < 732:
    _ = procure_dataset("lai_files",verbose=False)

# Get the shapefile for country borders
import requests
import shutil
from pathlib import Path

force = False
# zip file
zipfile = 'TM_WORLD_BORDERS-0.3.zip'
# URL
tm_borders_url = f"http://thematicmapping.org/downloads/{zipfile}"
# destibnation folder
destination_folder = Path('data')

# set up some filenames
zip_file = destination_folder.joinpath(zipfile)
shape_file = zip_file.with_name(zipfile.replace('zip', 'shp'))

# download zip if need to
if not Path(zip_file).exists():
    r = requests.get(tm_borders_url)
    with open(zip_file, 'wb') as fp:
        fp.write(r.content)

# extract shp from zip if need to
if force or not Path(shape_file).exists():
    shutil.unpack_archive(zip_file.as_posix(), extract_dir=destination_folder)
    

# Read the LAI dataset for a given country and year
# read in the LAI data for given country code
from geog0111.process_timeseries import process_timeseries
'''
Note, the saved npz file can be quite large
e.g. 8.1 G for France uncompressed, so we use compression.

You can override saving it by setting save = False
but if it is saved, it will be faster to access
data the next time you need it.

If you have a slow network, you might set download=False
'''
save = True
download = True
# want sigma as low as we can deal with, whilst 
# still interpolating effectively
sigma = 3


tiles = []
for h in [17, 18]:
    for v in [3, 4]:
        tiles.append(f"h{h:02d}v{v:02d}")
        
fname = f'lai_data_{year}_{country_code}.npz'
ofile = Path('data')/fname
done = False

if ofile.exists():
    done = True
    
# try to download it from server
if download:
    done = procure_dataset(fname,verbose=True)

import scipy
import scipy.ndimage.filters
if not done:
    # else generate it
    dates, lai_array, weights_array = process_timeseries(year,tiles,\
                                                     country_code=country_code)
    lai = {'dates':dates, 'lai':lai_array, 'weights':weights_array}
    if verbose: 
        print(np.nanmean(lai_array))
        print(np.nanmean(weights_array))

    # set up filter
    x = np.arange(-3*sigma,3*sigma+1)
    gaussian = np.exp((-(x/sigma)**2)/2.0)

    FIPS = country_code
    dates, lai_array, weights_array = lai['dates'],lai['lai'],lai['weights']
    print(lai_array.shape, weights_array.shape) #Check the output array shapes
    print('interpolating ...')
    numerator = scipy.ndimage.filters.convolve1d(lai_array * weights_array, gaussian, axis=2,mode='wrap')
    denominator = scipy.ndimage.filters.convolve1d(weights_array, gaussian, axis=2,mode='wrap')

    # avoid divide by 0 problems by setting zero values
    # of the denominator to not a number (NaN)
    denominator[denominator==0] = np.nan

    interpolated_lai = numerator/denominator
    print(interpolated_lai.shape)

    # need to convert to dict to be able to assign
    lai['interpolated_lai'] = interpolated_lai
    print('saving ...')



    if save:
        np.savez_compressed(ofile,**lai)

# Get the 2t dataset from ECMWF for Europe

from ecmwfapi import ECMWFDataServer
from pathlib import Path
from geog0111.geog_data import procure_dataset

ecmwf_file = 'europe_data_2016_2017.nc'

# pull the years info from ifile
# if the file is multiple years eg europe_data_2010_2011.nc
# then split it into multiple files
years = np.array(Path(ecmwf_file).stem.split('_'))[2:].astype(int)


if not (Path('data')/ecmwf_file).exists():
    # try to get it from UCL servers
    done = procure_dataset(ofile,verbose=True)
    if not done:
        server = ECMWFDataServer()
        print('requesting data ... may take some time')
        server.retrieve({
            "class": "ei",
            "dataset": "interim",
            "date": f"{years[0]}-01-01/to/{years[1]+1}-01-01", # Time period
            "expver": "1",
            "levtype": "sfc",
            "param": "2t",           # Parameters. Here we use 2m Temperature (2t)  See the ECMWF parameter database, at http://apps.ecmwf.int/codes/grib/param-db
            "stream": "oper",
            "type": "an",
            "time": "00/60/12/18",
            "step": "0",
            "area": "75/-20/10/60",    # Subset or clip to an area, here to Europe. Specify as North/West/South/East in Geographic lat/long degrees. Southern latitudes and Western longitudes must be given as negative numbers.
            "grid": "0.25/0.25",        # Regrid from the default grid to a regular lat/lon with specified resolution. The first number is east-west resolution (longitude) and the second is north-south (latitude).
            "format": "netcdf",         # Convert the output file from the default GRIB format to NetCDF format. Requires "grid" to be set to a regular lat/lon grid.
            "target": f"data/{ecmwf_file}",  # The output file name. Set this to whatever you like.
        })
else: print(f'{ecmwf_file} exists')



from osgeo import gdal
import requests
from pathlib import Path
import numpy as np

# download example grib file from
url = "http://gribs2.gmn-usa.com/cgi-bin/" +\
        "weather_fetch.pl?parameter=wind&days=7&region=Pacific&dataset=nww3"
ofile = 'data/Pacific.wind.7days.grb'
overwrite = False

# get the example grib datafile
# see
# https://gis.stackexchange.com/questions/
# 289314/using-gdal-to-read-data-from-grib-file-in-python
output_fname = Path(ofile)
if (not Path('data/grb.wkt').exists()) or \
    (not output_fname.exists()) or overwrite:

    with requests.Session() as session:
        r1 = session.request('get',url)
        if r1.url:
            r2 = session.get(r1.url)
            data = r2.content
            d = 0
            with open(output_fname, 'wb') as fp:
                d = fp.write(data)

    dataset = gdal.Open(ofile)
    wkt = dataset.GetProjection()
    with open('data/grb.wkt', 'w') as fp:
        # write wkt to file
        d = fp.write(wkt)
    
# test opening it
wkt2 = open('data/grb.wkt','r').readline()

print(wkt2)

from osgeo import gdal
import requests
from pathlib import Path
import numpy as np

'''
Get the SRS 6974 for MODIS
'''

url = 'http://spatialreference.org/ref/sr-org/6974/ogcwkt/'
ofile = 'data/modis_6974.wkt'
overwrite = False

# http://spatialreference.org/ref/sr-org/6974
output_fname = Path(ofile)

if overwrite or (not output_fname.exists()):
    with requests.Session() as session:
        r1 = session.request('get',url)
        if r1.url:
            r2 = session.get(r1.url)
            data = r2.text
            d = 0
            if overwrite or (not output_fname.exists()):  
                with open(output_fname, 'w') as fp:
                    d = fp.write(data)

# test opening it
wkt2 = open(ofile,'r').readline()

print(f'Refreshing nc file {ecmwf_file}')

import gdal
from datetime import datetime,timedelta
import numpy as np

ifile = f'data/{ecmwf_file}'

meta = gdal.Open(ifile).GetMetadata()
# get time info
timer = np.array([(datetime(1900,1,1) + timedelta(days=float(i)/24.)) \
for i in meta['NETCDF_DIM_time_VALUES'][1:-1].split(',')])

# filter data for required year

for year in years:
    ofile = f'data/europe_data_{year}.nc'
    mask = np.logical_and(timer >= datetime(year,1,1),timer <= datetime(year+1,1,1))
    timer2 = timer[mask]
    bands = ' '.join([f'-b {i}' for i in (np.where(mask)[0]+1)])    
    timer3 = '{'+','.join(np.array(meta['NETCDF_DIM_time_VALUES'][1:-1].split(','))[mask])+'}'
    timer4 = '{'+str(mask.sum())+',4}'
    options = f"-of netcdf -unscale -ot Float32 {bands} -mo NETCDF_DIM_time_VALUES={timer3}" + \
              f" -mo NETCDF_DIM_time_DEF={timer4} -a_srs data/grb.wkt"
    gdal.Translate(ofile+'tmp',ifile,options=options)
    Path(ofile+'tmp').replace(ofile)
    print(ofile)


### get land cover data

fname = f'landcover_data_{year}_{country_code}.npz'
ofile = Path('data')/fname
done = False

if ofile.exists():
    done = True

# try to download it from server
if download:
    done = procure_dataset(fname,verbose=True)

from geog0111.get_modis_files import get_modis_files
'''
Get the MODIS LC files from the server
to store in data
'''
try:
    url = 'https://e4ftl01.cr.usgs.gov//MODV6_Cmp_C/MOTA/'
    filename = get_modis_files(1,year,[tiles],base_url=url,\
                                               version=6,verbose=True,\
                                               destination_folder='data',\
                                               product='MCD12Q1')[0]
    print(filename)
except:
    print('server may be down')


from geog0111.process_timeseries import mosaic_and_clip

'''
Extract and clip the dataset
'''
lc_data = mosaic_and_clip(tiles,
                    1,
                    year,
                    folder='data',
                    layer="LC_Type3",
                    shpfile='data/TM_WORLD_BORDERS-0.3.shp',
                    country_code=country_code,
                    product='MCD12Q1',
                    frmat="MEM")

'''
Define LC table from userguide
https://lpdaac.usgs.gov/sites/default/\
        files/public/product_documentation/\
        mcd12_user_guide_v6.pdf
'''

table = '''
|Water Bodies|0|At least 60% of area is covered by permanent water bodies.|
|Grasslands|1|Dominated by herbaceous annuals (<2m) includ- ing cereal croplands.|
|Shrublands|2|Shrub (1-2m) cover >10%.|
|Broadleaf Croplands|3|Dominated by herbaceous annuals (<2m) that are cultivated with broadleaf crops.|
|Savannas|4|Between 10-60% tree cover (>2m).|
|Evergreen Broadleaf Forests|5|Dominated by evergreen broadleaf and palmate trees (>2m). Tree cover >60%.|
|Deciduous Broadleaf Forests|6|Dominated by deciduous broadleaf trees (>2m). Tree cover >60%.|
|Evergreen Needleleaf Forests|7|Dominated by evergreen conifer trees (>2m). Tree cover >60%.|
|Deciduous Needleleaf Forests|8|Dominated by deciduous needleleaf (larch) trees (>2m). Tree cover >60%.|
|Non-Vegetated Lands|9|At least 60% of area is non-vegetated barren (sand, rock, soil) or permanent snow and ice with less than 10% vegetation.|
|Urban and Built-up Lands|10|At least 30% impervious surface area including building materials, asphalt, and vehicles.|
|Unclassified|255|Has not received a map label because of missing inputs.|
'''

LC_Type3 = np.array([s.split('|')[1:-1] for s in table.split('\n')[1:-1]]).T
    

np.savez_compressed(f'data/landcover_{year}_{country_code}.npz',
                   LC_Type3=LC_Type3,lc_data=lc_data)


