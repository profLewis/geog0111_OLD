from osgeo import gdal, gdalconst,osr
import numpy as np
from geog0111.process_timeseries import mosaic_and_clip

def match_netcdf_to_data(src_filename,match_filename,dst_filename,\
                         country_code=country_code,shpfile=shpfile,\
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
    if verbose: print(f'writing to {dst_filename}')
    del dst # Flush
    return(dst_filename)
