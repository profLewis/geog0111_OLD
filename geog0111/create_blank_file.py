#!/usr/bin/env python

import gdal
from osgeo import gdalnumeric


__author__ = "P Lewis"
__copyright__ = "Copyright 2018 P Lewis"
__license__ = "GPLv3"
__email__ = "p.lewis@ucl.ac.uk"

def create_blank_file(input_filename,output_filename,value=255):
    '''
    following example in 
    http://geoexamples.blogspot.com/2012/12/raster-calculations-with-gdal-and-numpy.html

    Created GeoTiff format file called output_filename
    with same properties as input_filename.
    
    Limitations: this version limited to single band copy
    but could easily be extended by user

    input_filename  : string. Name of input file
    output_filename : string. Name of output file
    '''
    # open input and get data
    g = gdal.Open(input_filename,gdal.GA_ReadOnly)
    inband = g.GetRasterBand(1)
    indata = inband.ReadAsArray()
    
    # declare and open output and get data
    driver = gdal.GetDriverByName("GTiff")
    gOut = driver.Create(output_filename, g.RasterXSize, g.RasterYSize, 1, inband.DataType)
    outband = gOut.GetRasterBand(1)
    
    # write value to output
    # and copy other info
    gdalnumeric.BandWriteArray(outband,value+indata*0)
    gdalnumeric.CopyDatasetInfo(g,gOut)
    
    # close the file
    del gOut
    return(output_filename)
