import datetime

__author__ = "P Lewis"
__copyright__ = "Copyright 2018 P Lewis"
__license__ = "GPLv3"
__email__ = "p.lewis@ucl.ac.uk"

def today():
    '''
    returns (year,doy) for today

    '''
    d = datetime.date.today()
    d1 = datetime.datetime(d.year,d.month,d.day)
    d0 = datetime.datetime(d.year,1,1)
    doy = (d1 - d0).days
    year = d.year
    return (doy,year)
        
