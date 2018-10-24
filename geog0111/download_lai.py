#!/usr/bin/env python
'''
Python script to pull all MODIS files for LAI product for given years
for given tiles into destination_folder

'''

from geog0111.get_modis_files import get_modis_files
from datetime import datetime

years = [2017,2016]
tiles = ['h17v03', 'h18v03','h17v04', 'h18v04']
destination_folder = 'data'

for year in years:
    ndoys = (datetime(year,12,31) - datetime(year,1,1)).days + 1
    for doy in range(1,ndoys+1,4):
        print(year,ndoys,doy,end=' ')
        filenames = get_modis_files(doy,year,tiles,base_url='https://e4ftl01.cr.usgs.gov/MOTA',\
                                           version=6,\
                                           product='MCD15A3H')
        print(filenames)


