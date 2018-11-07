import numpy as np
import sys
import os
from pathlib import Path
import gdal
from datetime import datetime, timedelta


tiles = []
for h in [17, 18]:
    for v in [3, 4]:
        tiles.append(f"h{h:02d}v{v:02d}")


# get the MODIS LAI dataset for 2016/2017 for W. Europe
from geog0111.geog_data import procure_dataset
from pathlib import Path
import sys
year = 2017
if len(sys.argv) == 3:
    country_code = sys.argv[1]
    year = int(sys.argv[2])
elif len(sys.argv) == 2:
    country_code = sys.argv[1]
else:
    country_code = 'UK'
verbose = True

print(sys.argv,year,country_code)

### get land cover data

fname = f'data/landcover_{year}_{country_code}.npz'

ofile = Path('data')/fname
done = False

if ofile.exists():
    done = True

# try to download it from server
done = procure_dataset(fname,verbose=True)

from geog0111.get_modis_files import get_modis_files
from geog0111.process_timeseries import mosaic_and_clip

'''
Get the MODIS LC files from the server
to store in data
'''
if not done:
  try:
    url = 'https://e4ftl01.cr.usgs.gov//MODV6_Cmp_C/MOTA/'
    filename = get_modis_files(1,year,[tiles],base_url=url,\
                                               version=6,verbose=True,\
                                               destination_folder='data',\
                                               product='MCD12Q1')[0]
    print(filename)
  except:
    print('server may be down')


  '''
  Extract and clip the dataset
  '''
  lc_data = mosaic_and_clip(tiles,
                    1,
                    year,
                    folder='data',
                    layer="LC_Type3",
                    shpfile='data/TM_WORLD_BORDERS-0.3.shp',
                    country_code=country_code,
                    product='MCD12Q1',
                    frmat="MEM")

  '''
  Define LC table from userguide
  https://lpdaac.usgs.gov/sites/default/\
        files/public/product_documentation/\
        mcd12_user_guide_v6.pdf
  '''

  table = '''
|Water Bodies|0|At least 60% of area is covered by permanent water bodies.|
|Grasslands|1|Dominated by herbaceous annuals (<2m) includ- ing cereal croplands.|
|Shrublands|2|Shrub (1-2m) cover >10%.|
|Broadleaf Croplands|3|Dominated by herbaceous annuals (<2m) that are cultivated with broadleaf crops.|
|Savannas|4|Between 10-60% tree cover (>2m).|
|Evergreen Broadleaf Forests|5|Dominated by evergreen broadleaf and palmate trees (>2m). Tree cover >60%.|
|Deciduous Broadleaf Forests|6|Dominated by deciduous broadleaf trees (>2m). Tree cover >60%.|
|Evergreen Needleleaf Forests|7|Dominated by evergreen conifer trees (>2m). Tree cover >60%.|
|Deciduous Needleleaf Forests|8|Dominated by deciduous needleleaf (larch) trees (>2m). Tree cover >60%.|
|Non-Vegetated Lands|9|At least 60% of area is non-vegetated barren (sand, rock, soil) or permanent snow and ice with less than 10% vegetation.|
|Urban and Built-up Lands|10|At least 30% impervious surface area including building materials, asphalt, and vehicles.|
|Unclassified|255|Has not received a map label because of missing inputs.|
'''

  LC_Type3 = np.array([s.split('|')[1:-1] for s in table.split('\n')[1:-1]]).T
    

  np.savez_compressed(f'data/landcover_{year}_{country_code}.npz',
                   LC_Type3=LC_Type3,lc_data=lc_data)

