#!/usr/bin/env python
'''
Python script to pull all MODIS files for LAI product for given years
for given tiles into destination_folder

'''

from geog0111.get_modis_files import get_modis_files
from datetime import datetime

years = [2017,2016]
tiles = ['h09v05']
destination_folder = 'data'

for year in years:
    ndoys = (datetime(year,12,31) - datetime(year,1,1)).days + 1
    for doy in range(1,ndoys+1,1):
        print(year,ndoys,doy,end=' ')
        filenames = get_modis_files(doy,year,tiles,base_url='https://n5eil01u.ecs.nsidc.org/MOST',\
                                           version=6,
                                           product='MOD10A1')
        print(filenames)


