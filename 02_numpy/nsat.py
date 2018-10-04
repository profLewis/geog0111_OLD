#!/usr/bin/env python

import requests
import numpy as np

class nsat():
    '''
    Get information on the number of satellite launches
    for all months in some range of years
    
    Data scraped from https://www.n2yo.com for
    years year0 to year1 (not inclusive)
    
    __author__ = "P Lewis"
    __copyright__ = "Copyright 2018 P Lewis"
    __license__ = "GPLv3"
    __email__ = "p.lewis@ucl.ac.uk"
    
    '''

    def __init__(self,year0,year1):
        '''
        check to see if data table available
        else, scrape
        '''
        years = (year0,year1)
        try:
            data=np.loadtxt(f'satellites-{years[0]}-{years[1]}.gz')
        except:
            data = self.scrape_data(years)
            np.savetxt(f'satellites-{years[0]}-{years[1]}.gz',data,fmt='%d')
        self.data = data.astype(int)
            
    def scrape_data(self,years):
        # array of zeros
        nyears = years[1]-years[0]
        nmonths = 12

        data = np.zeros((nmonths,nyears),dtype=np.int)
        
        for i,year in enumerate(range(years[0],years[1])):
            for j,mon in enumerate(range(1,13)):
                # find number of satellite launches
                # by scraping https://www.n2yo.com/browse/
                url = f"https://www.n2yo.com/browse/?y={year}&m={mon:02d}"
                r = int(requests.get(url).text.count('<a href="/satellite/?s='))
                data[j,i] = r
        return data
