import datetime

__author__ = "P Lewis"
__copyright__ = "Copyright 2018 P Lewis"
__license__ = "GPLv3"
__email__ = "p.lewis@ucl.ac.uk"

class  get_url():
    '''
    get_url forms a full URL string associated with NASA Earthdata datasets

    '''
    def __init__(self,doy,year,product='MCD15A3H',version=6,\
 	              base_url='https://e4ftl01.cr.usgs.gov/MOTA'):
        '''

        Arguments:
        ----------
        doy  :   day of year (1 to 365 or 366 inclusive) (int)
        year :   year (int)

        Keyword arguments: 
        ------------------
        product:  MODIS product e.g. MCD15A3H as string
        base_url: dataset base URL e.g. https://e4ftl01.cr.usgs.gov/MOTA
                  as string
        version:  dataset version number (integer) e.g. 6

        Information available:
        ----------------------
        self.url
        self.year
        self.doy
        self.product
        self.base_url
        self.version
        self.ndays_in_year
     

        ''' 
        self.ndays_in_year = (datetime.datetime(year,12,31) - \
                                datetime.datetime(year,1,1)).days + 1

        if (doy < 1):
            print(f'Error: doy must be >= 1, not {doy}')
            return None
        if (doy > self.ndays_in_year):
            print(f'Error: doy must be <= {self.ndays_in_year}, not {doy} for year {year}')
            return None

        d = datetime.datetime(year,1,1) + datetime.timedelta(doy-1)
        datestr = f'{d.year:4d}.{d.month:02d}.{d.day:02d}'
        url = f'{base_url}/{product}.{version:03d}/{datestr}'

        self.url = url
        self.year = year
        self.doy = doy
        self.product = product
        self.base_url = base_url
        self.version = version

        return

