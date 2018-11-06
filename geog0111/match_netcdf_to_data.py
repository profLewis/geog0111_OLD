from osgeo import gdal, gdalconst,osr
import numpy as np
from geog0111.process_timeseries import mosaic_and_clip
from datetime import datetime , timedelta
from pathlib import Path



def match_netcdf_to_data(src_filename,match_filename,dst_filename,year,\
                         country_code=None,shpfile=None,force=False,\
                         nodata=-300,frmat='GTiff',verbose=False):

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
        if verbose: print('failed')
        return(None)

    # get meta data
    meta = gdal.Open(src_filename, gdalconst.GA_ReadOnly).GetMetadata()

    extent = [match_geotrans[0],match_geotrans[0]+match_geotrans[1]*wide,\
              match_geotrans[3]+match_geotrans[5]*high,match_geotrans[3]]
    # get time info
    timer = np.array([(datetime(1900,1,1) + timedelta(days=float(i)/24.)) \
         for i in meta['NETCDF_DIM_time_VALUES'][1:-1].split(',')])

    if (not Path(dst_filename).exists()) or force:

        '''
        Get geotrans, proj, data type and number of bands
        from source dataset
        '''
        band1 = src.GetRasterBand(1)
        src_geotrans = src.GetGeoTransform()
        src_proj = src.GetProjection()

        nbands = src.RasterCount
        src_format = band1.DataType

        dst = gdal.GetDriverByName('MEM').Create(\
                                        '', wide, high, \
                                        nbands, src_format)
        dst.SetGeoTransform( match_geotrans )
        dst.SetProjection( match_proj)

        if verbose: print(f'reprojecting ...')
            # Output / destination
        _ = gdal.ReprojectImage(src, dst, \
                                    src_proj, \
                                    match_proj,\
                                    gdalconst.GRA_Bilinear )
        if verbose: print(f'cropping to {country_code:s} ...')
        done = gdal.Warp(dst_filename,
                        dst,
                        format=frmat,
                        dstNodata=nodata,
                        cutlineDSName=shpfile,
                        cutlineWhere=f"FIPS='{country_code:s}'",
                        cropToCutline=True)
        del dst
 
    return(timer,dst_filename,extent)

