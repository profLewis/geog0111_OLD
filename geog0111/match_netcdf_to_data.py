from osgeo import gdal, gdalconst,osr
import numpy as np
from geog0111.process_timeseries import mosaic_and_clip
from datetime import datetime,timedelta



def match_netcdf_to_data(src_filename,match_filename,dst_filename,\
                         xoff = 0, yoff = 40, \
                         country_code='LU',shpfile="data/TM_WORLD_BORDERS-0.3.shp",\
                         nodata=-32767,frmat='GTiff',verbose=False):
    '''
    see :
    https://stackoverflow.com/questions/10454316/
    how-to-project-and-resample-a-grid-to-match-another-grid-with-gdal-python
    '''

    '''
    Get the projection, geotransform and dataset
    size that we want to match to
    '''
    if verbose: print(f'getting info from match file {match_filename}')
    match_ds = gdal.Open(match_filename, gdalconst.GA_ReadOnly)
    match_proj = match_ds.GetProjection()
    match_geotrans = match_ds.GetGeoTransform()
    wide = match_ds.RasterXSize
    high = match_ds.RasterYSize
    # close the file -- we dont need it any more
    del match_ds

    '''
    access information from source
    '''
    if verbose: print(f'getting info from source netcdf file {src_filename}')
    try:
        src_dataname = 'NETCDF:"'+src_filename+'":t2m'
        src = gdal.Open(src_dataname, gdalconst.GA_ReadOnly)
    except:
        return(None)
    
    '''
    Get geotrans, data type and number of bands
    from source dataset
    '''
    band1 = src.GetRasterBand(1)
    src_geotrans = src.GetGeoTransform()
    nbands = src.RasterCount
    src_format = band1.DataType
   

    # try to get the src projection 
    src_proj = src.GetProjection ()

    # if (when) we fail, tell it its wgs84
    if len(src_proj) == 0:
        # set up a spatial reference
        # as wgs84 
        wgs84 = osr.SpatialReference ()
        wgs84.ImportFromEPSG ( 4326 )
        src_proj = wgs84.ExportToWkt()
 
        
    if verbose: print(f'setting transform and projection info')
    if shpfile:
        dst = gdal.GetDriverByName('MEM').Create(\
                                    '', wide, high, \
                                    nbands, src_format)
    else:
        dst = gdal.GetDriverByName(frmat).Create(\
                                    dst_filename, wide, high, \
                                    nbands, src_format)
        
    dst.SetGeoTransform( match_geotrans )
    dst.SetProjection( match_proj)

    # Do the work: reproject the dataset
    if verbose: print(f'reprojecting ...')
    _ = gdal.ReprojectImage(src, dst, src_proj, match_proj, gdalconst.GRA_Bilinear)

    if shpfile:
        if verbose: print(f'cropping to {country_code:s}...')
        # Output / destination
        gdal.Warp(dst_filename,
                    dst,
                    format=frmat,
                    dstNodata=nodata,
                    cutlineDSName=shpfile,
                    cutlineWhere=f"FIPS='{country_code:s}'",
                cropToCutline=True)
    xOrigin = match_geotrans[0]
    yOrigin = match_geotrans[3]
    pixelWidth = match_geotrans[1]
    pixelHeight = match_geotrans[5]
    # the +40 pixels in y is to reconcile gdal and cartoply
    # it may be related to different ellispoids presumed
    # It is likely to be different elsewhere but still a y-shift
    # Its not important as we are using cartoply only to visiualise
    extent = (xOrigin+xoff*pixelWidth,xOrigin+pixelWidth*(xoff+wide),\
         yOrigin+pixelHeight*(high+yoff),yOrigin+yoff*pixelHeight)



    if verbose: print(f'writing to {dst_filename}')
    del dst # Flush


    return(extent)


def calibrate_t2(dst_filename,meta):
    '''
    apply scaling etc to temperature data t 2m
    '''
    # get time info
    timer = np.array([(datetime(1900,1,1) + timedelta(days=float(i)/24.)) \
         for i in meta['NETCDF_DIM_time_VALUES'][1:-1].split(',')])

    t2 = gdal.Open(dst_filename, gdalconst.GA_ReadOnly)
    t2 = np.array([t2.GetRasterBand(i+1).ReadAsArray() \
                   for i in range(timer.shape[0])])
    offset = float(meta['t2m#add_offset'])
    scale = float(meta['t2m#scale_factor'])
    missing = int(meta['t2m#missing_value'])
    # set missing to nan
    nodata = (t2 == missing)
    # convert to C
    temp2 = t2 * scale + offset - 273.15
    temp2[nodata] = np.nan
    return timer,temp2



