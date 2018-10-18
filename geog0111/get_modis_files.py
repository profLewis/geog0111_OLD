import datetime
from bs4 import BeautifulSoup
from geog0111.cylog import cylog
from geog0111.get_url import get_url
import requests
from pathlib import Path
import numpy as np

__author__ = "P Lewis"
__copyright__ = "Copyright 2018 P Lewis"
__license__ = "GPLv3"
__email__ = "p.lewis@ucl.ac.uk"

'''
forms a full URL string associated with NASA Earthdata datasets
for given doy, year and tiles
'''
def get_modis_files(doy,year,tiles,product='MCD15A3H',version=6,\
                      destination_folder='data',verbose=False,\
 	              base_url='https://e4ftl01.cr.usgs.gov/MOTA'):
        '''

        Arguments:
        ----------
        doy  :   day of year (1 to 365 or 366 inclusive) (int)
        year :   year (int)
        tiles:   list of tiles

        Keyword arguments: 
        ------------------
        verbose:  priont some useful information
        product:  MODIS product e.g. MCD15A3H as string
        base_url: dataset base URL e.g. https://e4ftl01.cr.usgs.gov/MOTA
                  as string
        version:  dataset version number (integer) e.g. 6
        destination_folder:  destination folder
        ''' 
        ndays_in_year = (datetime.datetime(year,12,31) - \
                                datetime.datetime(year,1,1)).days + 1

        if (doy < 1):
            print(f'Error: doy must be >= 1, not {doy}')
            return None
        if (doy > ndays_in_year):
            print(f'Error: doy must be <= {ndays_in_year}, not {doy} for year {year}')
            return None

        d = datetime.datetime(year,1,1) + datetime.timedelta(doy-1)
        datestr = f'{d.year:4d}.{d.month:02d}.{d.day:02d}'

        url = f'{base_url}/{product}.{version:03d}/{datestr}'

        tile_urls = []

        with requests.Session() as session:
            # get password-authorised url
            session.auth = cylog().login()
            r1 = session.request('get',url)
            # this gets the url with codes for login etc.
            r2 = session.get(r1.url)
            html = r2.text

            links = [mylink.attrs['href'] for mylink in BeautifulSoup(html,'lxml').find_all('a')]

            tile_url = [item for item in links \
                      if (item.split('.')[-1] == 'hdf') and \
                         (item.split('.')[-4] in tiles)]
            tile_url = np.unique(tile_url)

            tile_urls = [f'{url}/{u}' for u in tile_url]


        outfiles = []
        # loop over urls
        for url in tile_urls:
    
            # get the filename from the url
            filename = url.split('/')[-1]
            if verbose: print(filename)
    
            # make sure destination_folder exists
            dest_path = Path(destination_folder)
            if not dest_path.exists():
                dest_path.mkdir()
    
            # make a compound file name from folder and filename
            output_fname = dest_path.joinpath(filename)
    
            # does the file already exist?
            if not output_fname.exists():
                # put download and save code here
                with requests.Session() as session:
                    # get password-authorised url
                    session.auth = cylog().login()
                    r1 = session.request('get',url)
                    # this gets the url with codes for login etc.
                    r2 = session.get(r1.url)
                    with open(output_fname, 'wb') as fp:
                        r = fp.write(r2.content)
            else:
                if verbose: print(f'{output_fname} exists')
            outfiles.append(str(output_fname))

        return outfiles
