import numpy as np
import matplotlib.pylab as plt

def plot_land_cover(lc_data,year,country_code,cmap='tab20b'):
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
    

    '''
    First, lets get the codes and names of the LCs used
    '''
    flc_data = lc_data.astype(float)
    flc_data[lc_data == 255] = np.nan
    land_covers_present = np.unique(lc_data[lc_data!=255])
    land_cover_names = LC_Type3[0]
    '''
    For categorical data we want a quantitative colormap

    The core options are:
    https://matplotlib.org/tutorials/colors/colormaps.html

    qcmaps = ['Pastel1', 'Pastel2', 'Paired', 'Accent',
             'Dark2', 'Set1', 'Set2', 'Set3',
              'tab10', 'tab20', 'tab20b', 'tab20c']
    '''

    '''
    Now learn how to plot with categorical labels
    following example in
    https://gist.github.com/jakevdp/8a992f606899ac24b711
    FuncFormatter to put labels 
    '''

    ncov = land_covers_present.max()
    # This function formatter will replace integers with target names
    formatter = plt.FuncFormatter(lambda val, loc: land_cover_names[val])
    plt.figure(figsize=(10,10))
    plt.title(f'MODIS LAI Land cover LC_Type3 from MCD12Q1 {year} {country_code}')
    plt.imshow(flc_data,vmin=0,vmax=ncov,\
               cmap=plt.cm.get_cmap(cmap,ncov))
    plt.colorbar(ticks=np.arange(ncov+2).astype(int), \
                 format=formatter)
    return(land_cover_names[land_covers_present]) 
