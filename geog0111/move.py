from geog0111.geog_data import *

destination_folder = Path('data')
if not destination_folder.exists():
        dest_path.mkdir()

# we have the filenames provided 
# in data/lai_filelist_2016.dat.txt
for year in [2016,2017]:
    control_file = f'data/lai_filelist_{year}.dat.txt'
    # read the ascii data from the file in
    filenames = open(control_file).read().split()

    # get the local files
    # set verbose=True if you want to see what is happening
    done = [procure_dataset(f,\
                verbose=False,\
                destination_folder=destination_folder) 
                                    for f in filenames]
    # done should be all True if this has worked

    # print the first 8 in the list, just to see it looks ok
    print(f'\n {year}\n','*'*len(str(year)))
    for f in filenames[:8]:
        print (f)


import requests
import shutil 
from pathlib import Path

# zip file
zipfile = 'TM_WORLD_BORDERS-0.3.zip'
# URL
tm_borders_url = f"http://thematicmapping.org/downloads/{zipfile}"
# destibnation folder
destination_folder = Path('data')

# set up some filenames
zip_file = destination_folder.joinpath(zipfile)
shape_file = zip_file.with_name(zipfile.replace('zip','shp'))

# download zip if need to
if not Path(zip_file).exists():
    r = requests.get(tm_borders_url)
    with open(zip_file, 'wb') as fp:
        fp.write (r.content)

# extract shp from zip if need to
if not Path(shape_file).exists():
    shutil.unpack_archive(zip_file.as_posix(),
                         extract_dir=destination_folder)

import gdal
import numpy as np
from pathlib import Path
from geog0111.create_blank_file import create_blank_file
from datetime import datetime

destination_folder = Path('data')
year = 2017
product = 'MCD15A3H'
version = 6
tile = 'h1[7-8]v0[3-4]'
FIPS = "SP"

tile_ = tile.replace('[','_').replace(']','_').replace('-','')+FIPS

shape_file = destination_folder.\
                 joinpath('TM_WORLD_BORDERS-0.3.shp').as_posix()

doy = 149

ipfile = destination_folder.\
                joinpath(f'{product}.A{year}{doy:03d}.{tile_}.{version:03d}').as_posix()

opfile = ipfile.replace(f'{doy:03d}.','').replace(tile,tile_)

filenames = list(destination_folder\
                .glob(f'{product}.A{year}{doy:03d}.{tile}.{version:03d}.*.hdf'))

ofiles = []
params =  ['Lai_500m', 'FparLai_QC']
for d in params:
    dataset_names = sorted([f'HDF4_EOS:EOS_GRID:'+\
                         f'"{file_name.as_posix()}":'+\
                         f'MOD_Grid_MCD15A3H:{d}'\
                            for file_name in filenames])

    spatial_file = f'{opfile}.{doy:03d}.{d}.vrt'
    clipped_file = f'{opfile}.{doy:03d}_clip.{d}.vrt'
    g = gdal.BuildVRT(spatial_file, dataset_names)
    if(g):
        del(g)
        g = gdal.Warp(clipped_file,\
                                   spatial_file,\
                                   format='VRT', dstNodata=255,\
                                   cutlineDSName=shape_file,\
                                   cutlineWhere=f"FIPS='{FIPS}'",\
                                   cropToCutline=True)
        if (g):
            del(g)
        ofiles.append(clipped_file)
print(ofiles)

lai = [gdal.Open(ofiles[i]).ReadAsArray() for i in range(len(params))]

lai[0] = lai[0] * 0.1
# if we want bit field 5-7
# we form a binary mask
mask57 = 0b11100000
# and right shift 5 (>> 5)
lai[1] = (lai[1] & mask57) >> 5
# 0 to 3 are good
scale = 0.61803398875
lai[1] = (scale**0) * (lai[1] == 0).astype(float) + \
         (scale**1) * (lai[1] == 1).astype(float) + \
         (scale**2) * (lai[1] == 2).astype(float) + \
         (scale**3) * (lai[1] == 3).astype(float)
    

import gdal
import numpy as np
from pathlib import Path
from geog0111.create_blank_file import create_blank_file
from datetime import datetime

destination_folder = Path('data')
year = 2017
product = 'MCD15A3H'
version = 6
tile = 'h1[7-8]v0[3-4]'
params =  ['Lai_500m', 'FparLai_QC']



tile_ = tile.replace('[','_').replace(']','_').replace('-','')+FIPS

shape_file = destination_folder.\
                 joinpath('TM_WORLD_BORDERS-0.3.shp').as_posix()

allopfile = destination_folder.\
                joinpath(f'{product}.A{year}.{tile_}.{version:03d}')

ndays_in_year = (datetime(year,12,31) - datetime(year,1,1)).days + 1

for d in params:
    old_clip = None
    allvrt = []
    bandNames = []
    for doy in range(1,ndays_in_year+1,1):
        print(doy,'...',end=' ')
        ipfile = destination_folder.\
                    joinpath(f'{product}.A{year}{doy:03d}.{tile_}.{version:03d}').as_posix()

        opfile = ipfile.replace(f'{doy:03d}.','').replace(tile,tile_)

        filenames = destination_folder\
                    .glob(f'{product}.A{year}{doy:03d}.{tile}.{version:03d}.*.hdf')

        dataset_names = sorted([f'HDF4_EOS:EOS_GRID:'+\
                             f'"{file_name.as_posix()}":'+\
                             f'MOD_Grid_MCD15A3H:{d}'\
                                for file_name in filenames])
        spatial_file = f'{opfile}.{doy:03d}.{d}.vrt'
        clipped_file = f'{opfile}.{doy:03d}_clip.{d}.vrt'
        if len(dataset_names):
            g = gdal.BuildVRT(spatial_file, dataset_names)
            if(g):
                del(g)
                g = gdal.Warp(clipped_file,\
                                   spatial_file,\
                                   format='VRT', dstNodata=255,\
                                   cutlineDSName=shape_file,\
                                   cutlineWhere=f"FIPS='{FIPS}'",\
                                   cropToCutline=True)
        elif old_clip:
            blank_file_tiff = f'{opfile}_blank.tiff'
            # generate a blank dataset in case of missing days
            if not Path(blank_file_tiff).exists():
                # copy info
                create_blank_file(old_clip,blank_file_tiff,value=255)

            # build a vrt
            g = gdal.BuildVRT(clipped_file, [blank_file_tiff])

        if (g):
            del(g)
            bandNames.append(f'DOY {doy:03d}')
            allvrt.append(clipped_file)

        old_clip = clipped_file



    g = gdal.BuildVRT(f'{allopfile.as_posix()}.{d}.vrt', allvrt,\
                      options=gdal.BuildVRTOptions(VRTNodata=255,\
                                                   srcNodata=255,\
                                                   allowProjectionDifference=True,\
                                                   separate=True))
    if (g):
        # set band names
        for i in range(g.RasterCount):
            g.GetRasterBand(i+1).SetDescription(bandNames[i])

        # close and flush file
        del g
        print (f'{allopfile.as_posix()}.{d}.vrt')

import gdal
import numpy as np

destination_folder = Path('data')
year = 2017
product = 'MCD15A3H'
version = 6
tile = 'h1[7-8]v0[3-4]'
params =  ['Lai_500m', 'FparLai_QC']

allopfile = destination_folder.\
                joinpath(f'{product}.A{year}.{tile_}.{version:03d}')
lai = []
for d in params:
    
    g = gdal.Open(f'{allopfile.as_posix()}.{d}.vrt',gdal.GA_ReadOnly)
    data = np.array([g.GetRasterBand(b+1).ReadAsArray() \
                for b in range(g.RasterCount)])

    lai.append(data)

lai[0] = lai[0] * 0.1
# if we want bit field 5-7
# we form a binary mask
mask57 = 0b11100000
# and right shift 5 (>> 5)
lai[1] = (lai[1] & mask57) >> 5
# 0 to 3 are good
scale = 0.61803398875
lai[1] = (scale**0) * (lai[1] == 0).astype(float) + \
         (scale**1) * (lai[1] == 1).astype(float) + \
         (scale**2) * (lai[1] == 2).astype(float) + \
         (scale**3) * (lai[1] == 3).astype(float)
    
print(lai[0].shape)

import scipy.ndimage.filters
import matplotlib.pylab as plt

weight = lai[1]

# filter, in units of days
sigma = 8
gx = np.arange(-3*sigma, 3*sigma, 1)
gaussian = np.exp(-(gx/sigma)**2/2.)
plt.plot(gx,gaussian)
x = scipy.ndimage.filters.convolve1d(lai[0] * weight, gaussian, axis=0,mode='wrap')
w = scipy.ndimage.filters.convolve1d(weight, gaussian, axis=0,mode='wrap')
ilai = x/w

import imageio
import tempfile

# lai movie as animated gif

destination_folder = Path('images')
year = 2017
product = 'MCD15A3H'
version = 6
tile = 'h1[7-8]v0[3-4]'
params =  ['Lai_500m', 'FparLai_QC']

tile_ = tile.replace('[','_').replace(']','_').replace('-','')+FIPS
allopfile = destination_folder.\
                joinpath(f'{product}.A{year}.{tile_}.{version:03d}')

images = []
with tempfile.TemporaryDirectory() as tmpdirname:
    ofile = f'{tmpdirname}/tmp.png'
    
    for i in range(ilai.shape[0]):
        print(i,'...',end=' ')
        plt.figure(0,figsize=(10,6))
        plt.clf()
        plt.imshow(ilai[i],vmin=0,vmax=6,cmap=plt.cm.inferno_r)
        plt.title(f'{product} {FIPS} {params[0]} {year} DOY {i+1:03d}')
        plt.colorbar(shrink=0.85)
        plt.savefig(ofile)    
        images.append(imageio.imread(ofile))
imageio.mimsave(f'{allopfile}.gif', images)
print(f'{allopfile}.gif')

