.. SIAC documentation master file, created by
   sphinx-quickstart on Thu Nov  8 18:01:40 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

A sensor invariant Atmospheric Correction (SIAC)
================================================

This atmospheric correction method uses MODIS MCD43 BRDF product to get
a coarse resolution simulation of earth surface. A model based on MODIS
PSF is built to deal with the scale differences between MODIS and other
sensors, and linear spectral mapping is used to map between different
sensors spectrally. We uses the ECMWF
`CAMS <http://apps.ecmwf.int/datasets/data/cams-nrealtime/levtype=sfc/>`__
prediction as a prior for the atmospheric states, coupling with 6S model
to solve for the atmospheric parameters, then the solved atmospheric
parameters are used to correct the TOA reflectances. The whole system is
built under Bayesian theory and the uncertainty is propagated through
the whole system. Since we do not rely on specific bands' relationship
to estimate the atmospheric states, but instead a more generic and
consistent way of inversion those parameters. The code can be downloaded
from `SIAC <https://github.com/MarcYin/Atmospheric_correction>`__ github
directly and futrher updates will make it more independent and can be
installed on different machines.



Development of this code has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 687320, under project H2020 MULTIPLY.
f this code has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 687320, under project `H2020 MULTIPLY <http://www.multiply-h2020.eu/>`_.



.. toctree::
   :maxdepth: 2
   :caption: Contents:

    Chapter0_help.rst
    Chapter1_Python_introduction_answers.rst
    Chapter1_Python_introduction.rst
    Chapter2_Numpy_matplotlib_answers.rst
    Chapter2_Numpy_matplotlib.rst
    Chapter3_0_GDAL.rst
    Chapter3_1_GDAL_answers.rst
    Chapter3_1_GDAL.rst
    Chapter3_2_MODIS_download_answers.rst
    Chapter3_2_MODIS_download.rst
    Chapter3_3_GDAL_masking.rst
    Chapter3_4a_GDAL_stacking_and_interpolating-convolution.rst
    Chapter3_4_GDAL_stacking_and_interpolating.rst
    Chapter3_5_Movies.rst
    Chapter3_6A_GDAL_Reconciling_projections_prerequisites.rst
    Chapter3_6_GDAL_Reconciling_projections.rst
    Chapter4_Practical_Part1.rst
    Chapter5_Linear_models.rst
    Chapter5_Modelling_and_optimisation.rst
    Chapter6_NonLinear_Model_Fitting.rst
    Chapter6_NonLinear_Model_Fitting_Solutions.rst
    Chapter7_FittingPhenologyModels.rst
    Chapter7_FittingPhenologyModels_Solutions.rst
    Chapter8_Practical_Part2.rst
    Chapter9_Fire_and_Teleconnections.rst
    Chapter9_Fire_and_Teleconnections_Solution.rst
    Connection.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
