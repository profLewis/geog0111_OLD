
3 Geospatial processing with ``gdal``
=====================================

.. raw:: html

   <h1>

Table of Contents

.. raw:: html

   </h1>

.. container:: toc

   .. raw:: html

      <ul class="toc-item">

   .. raw:: html

      </ul>

`GDAL <https://gdal.org>`__ is the workhorse of geospatial processing.
Basically, GDAL offers a common library to access a vast number of
formats (if you want to see how vast, `check
this <https://gdal.org/formats_list.html>`__). In addition to letting
you open and convert obscure formats to something more useful, a lot of
functionality in terms of processing raster data is available (for
example, working with projections, combining datasets, accessing remote
datasets, etc).

For vector data, the counterpart to GDAL is OGR (which is now a part of
the GDAL library anyway), which also supports `many vector
formats <https://gdal.org/ogr_formats.html>`__. The combination of both
libraries is a very powerful tool to work with geospatial data, not only
from Python, but from `many other popular computer
languages <https://trac.osgeo.org/gdal/#GDALOGRInOtherLanguages>`__.

In this session, we will introduce the ``gdal`` geospatial module which
can read a wide range of raster scientific data formats. We will also
introduce the related ``ogr`` vector package.

In pacticular, we will learn how to:

-  access and download NASA geophysical datasets (specifically, the
   MODIS LAI/FPAR product)
-  apply a vector mask to the dataset
-  apply quality control flags to the data
-  stack datasets into a 3D numpy dataset for further analysis,
   including interpolation of missing values
-  visualise the data
-  store the stacked dataset

**These are all tasks that you will be required to do for the**\ `part 1
formal assessment <Formal_assessment_part1.ipynb>`__\ **of this course.
You will however be using a different NASA dataset.**

3.1 MODIS LAI product
---------------------

To introduce geospatial processing, we will use a dataset from the MODIS
LAI product over the UK.

You should note that the dataset you need to use for your assessed
practical is a MODIS dataset with similar characteristics to the one in
this example.

The data product
`MOD15 <https://modis.gsfc.nasa.gov/data/dataprod/mod15.php>`__ LAI/FPAR
has been generated from NASA MODIS sensors Terra and Aqua data since
2002. We are now in dataset collection 6 (the data version to use).

::

   LAI is defined as the one-sided green leaf area per unit ground area in broadleaf canopies and as half the total needle surface area per unit ground area in coniferous canopies. FPAR is the fraction of photosynthetically active radiation (400-700 nm) absorbed by green vegetation. Both variables are used for calculating surface photosynthesis, evapotranspiration, and net primary production, which in turn are used to calculate terrestrial energy, carbon, water cycle processes, and biogeochemistry of vegetation. Algorithm refinements have improved quality of retrievals and consistency with field measurements over all biomes, with a focus on woody vegetation.

We use such data to map and understand about the dynamics of terrestrial
vegetation / carbon, for example, for climate studies.

The raster data are arranged in tiles, indexed by row and column, to
cover the globe:

.. figure:: https://www.researchgate.net/profile/J_Townshend/publication/220473201/figure/fig5/AS:277546596880390@1443183673583/The-global-MODIS-Sinusoidal-tile-grid.png
   :alt: MODIS tiles

   MODIS tiles

**Exercise 3.1.1**

The pattern on the tile names is ``hXXvYY`` where ``XX`` is the
horizontal coordinate and ``YY`` the vertical.

-  use the map above to work out the names of the two tiles that we will
   need to access data over the UK
-  set the variable ``tiles`` to contain these two names in a list

For example, for the two tiles covering Madegascar, we would set:

::

   tiles = ['h22v10','h22v11']

.. code:: python

    # do exercise here
    # ANSWER 
    
    tiles = ['h17v03','h17v03']

3.1.1 NASA Earthdata access
~~~~~~~~~~~~~~~~~~~~~~~~~~~

3.1.1.1 Register at NASA Earthdata
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before you attempt to do this section, you will need to register at
`NASA Earthdata <https://urs.earthdata.nasa.gov/home>`__.

We have set up these notes so that you don’t have to put your username
and password in plain text. Instead, you need to enter your username and
password when prompted by ``cylog``. The password is stored in an
encrypted file, although it can be accessed as plain text within your
Python session.

**N.B. using ``cylog().login()`` is only intended to work with access to
NASA Earthdata and to prevent you having to expose your username and
password in these notes**.

``cylog().login()`` returns the tuple ``(username,password)`` in plain
text.

.. code:: python

    import geog0111.nasa_requests as nasa_requests
    from geog0111.cylog import cylog
    %matplotlib inline
    
    url = 'https://e4ftl01.cr.usgs.gov/MOTA/MCD15A3H.006/2018.09.30/' 
            
    # grab the HTML information
    try:
        html = nasa_requests.get(url).text
        # test a few lines of the html
        if html[:20] == '<!DOCTYPE HTML PUBLI':
            print('this seems to be ok ... ')
            print('use cylog().login() anywhere you need to specify the tuple (username,password)')
    except:
        print('login error ... try entering your username password again')
        print('then re-run this cell until it works')
        cylog(init=True)

The NASA servers go down for weekly maintenance, usually on Wednesday
afternoon (UK time), so you might not want to attempt this exercise
then.

3.1.2 ``gdal``
--------------

We should now check to see if you have ``gdal`` properly installed.

.. code:: python

    import gdal
    version = gdal.VersionInfo()  
    
    if int(version) >= 2020400:
        print('gdal ok',version)
    else:
        print('gdal problem',version,'2.2.4+ expected')

If there is a problem and you are on the geography system, we should be
able to fix it for you.

If you are not on the geography system, try running:

::

   conda env update -f environment.yml 

before going any further. If an update occurs, shutdown and restart your
notebooks.

3.2 Automatic downloading of NASA MODIS products
------------------------------------------------

In `this section <Chapter3_2_MODIS_download.ipynb>`__, you will learn
how to:

-  scan the directories (on the Earthdata server) where the MODIS data
   are stored
-  get the dataset filename for a given tile, date and product
-  get to URL associated with the dataset
-  use the URL to pull the dataset over to store in the local file
   system

3.3 GDAL masking
----------------

In `this section <Chapter3_3_GDAL_masking.ipynb>`__ you will learn how
to:

-  load locally stored files into gdal
-  select a particular dataset
-  form a virtual ‘stitched’ dataset from multiple files
-  apply a mask to the data from a vector boundary
-  crop the dataset

3.4 GDAL stacking and interpolating
-----------------------------------

In `this section <Chapter3_4_GDAL_stacking_and_interpolating.ipynb>`__
you will learn how to:

-  generate a numpy time series of spatial data
-  interpolate/smooth the dataset

3.5 Summary
-----------

In this session, we have learned to use some geospatial tools using GDAL
in Python. A good set of `working notes on how to use
GDAL <http://jgomezdans.github.io/gdal_notes/>`__ has been developed
that you will find useful for further reading, as well as looking at the
`advanced <advanced.ipynb>`__ section.

We have also very briefly introduced dealing with vector datasets in
``ogr``, but this was mainly through the use of a pre-defined function
that will take an ESRI shapefile (vector dataset), warp this to the
projection of a raster dataset, and produce a mask for a given layer in
the vector file.

If there is time in the class, we will develop some exercises to examine
the datasets we have generated and/or to explore some different datasets
or different locations.
