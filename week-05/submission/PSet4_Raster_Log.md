# Problem Set 4: Working With Landsat Data

## Description

Your challenge this week is to package the functionality we were working with in the workshop into a series of functions capable of processing Landsat data. You'll then use these functions to process Landsat data you've downloaded, producing estimates of Vegetation Land Surface Temperature. Finally, you'll use the BQA band to write a filter that removes clouds and cloud shadows from our Landsat dataset.

## Deliverables

### To GitHub

1. Your Python functions, pushed to your Github week-05 submission folder. Use this markdown page as a template!

### To Stellar

**NOTE: Your compressed `tifs` should each be between 90 and 150 MB.**

1. Your NDVI `tif`, compressed into a `zip` file, with clouds filtered. Call this file `yourlastname_ndvi_imagerydate.zip` (where `imagerydate` is the date the image was captured in the format `YYYYMMDD`).
2. Your Land Surface Temperature `tif`, compressed into a `zip` file with clouds filtered. Call this file `yourlastname_lst_imagerydate.zip` (where `imagerydate` is the date the image was captured in the format `YYYYMMDD`).

## Code from Class

```python
import sys
sys.path.insert(0,'/Library/Frameworks/GDAL.framework/Versions/2.2/Python/3.6/site-packages')
from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np
import os
%matplotlib inline

DATA = "/Users/cristinalogg/Desktop/LC08_L1TP_012031_20170614_20170628_01_T1"

def process_string (st):
    """
    Parses Landsat metadata
    """
    return float(st.split(' = ')[1].strip('\n'))

def ndvi_calc(red, nir):
    """
    Calculate NDVI
    """
    return (nir - red) / (nir + red)

def emissivity_calc (pv, ndvi):
    """
    Calculates an estimate of emissivity
    """
    ndvi_dest = ndvi.copy()
    ndvi_dest[np.where(ndvi < 0)] = 0.991
    ndvi_dest[np.where((0 <= ndvi) & (ndvi < 0.2)) ] = 0.966
    ndvi_dest[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ] = (0.973 * pv[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ]) + (0.966 * (1 - pv[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ]) + 0.005)
    ndvi_dest[np.where(ndvi >= 0.5)] = 0.973
    return ndvi_dest

def array2tif(raster_file, new_raster_file, array):
    """
    Writes 'array' to a new tif, 'new_raster_file',
    whose properties are given by a reference tif,
    here called 'raster_file.'
    """
    # Invoke the GDAL Geotiff driver
    raster = gdal.Open(raster_file)

    driver = gdal.GetDriverByName('GTiff')
    out_raster = driver.Create(new_raster_file,
                        raster.RasterXSize,
                        raster.RasterYSize,
                        1,
                        gdal.GDT_Float32)
    out_raster.SetProjection(raster.GetProjection())
    # Set transformation - same logic as above.
    out_raster.SetGeoTransform(raster.GetGeoTransform())
    # Set up a new band.
    out_band = out_raster.GetRasterBand(1)
    # Set NoData Value
    out_band.SetNoDataValue(-1)
    # Write our Numpy array to the new band!
    out_band.WriteArray(array)

```
# Your Functions!

We recommend reading carefully through the goals for all functions before starting the first function.

```python
def tif2array(location):
  raster = os.path.join(DATA, location) #Read in the file
  data = gdal.Open(raster) #Load in the B1 Data
  band = data.GetRasterBand(1) #Load in the B1 Data
  array = data.ReadAsArray() #Load in the B1 Data
  floatarray = array.astype(np.float32) #Convert array to type Float 32
  return floatarray
    """
    Should:
    1. Use gdal.open to open a connection to a file.
    2. Get band 1 of the raster
    3. Read the band as a numpy array
    4. Convert the numpy array to type 'float32'
    5. Return the numpy array.
    """

def retrieve_meta(meta_text):
  with open(meta_text) as f:
    meta = f.readlines()
  matchers = ['RADIANCE_MULT_BAND_10', 'RADIANCE_ADD_BAND_10', 'K1_CONSTANT_BAND_10', 'K2_CONSTANT_BAND_10']
  matching = [process_string(s) for s in meta if any(xs in s for xs in matchers)]
  return matching
    """
    Retrieve variables from the Landsat metadata *_MTL.txt file
    Should return a list of length 4.
    'meta_text' should be the location of your metadata file
    Use the process_string function we created in the workshop.
    """

def rad_calc(tirs, var_list):
  rad = Band10Meta[0] * tirs + Band10Meta[1]
  return rad
    """
    Calculate Top of Atmosphere Spectral Radiance
    Note that you'll have to access the metadata variables by
    their index number in the list, instead of naming them like we did in class.
    """

def bt_calc(rad, var_list):
  bt = Band10Meta[3] / np.log((Band10Meta[2]/rad) + 1) - 273.15
  return bt
  """
    Calculate Brightness Temperature
    Again, you'll have to access appropriate metadata variables
    by their index number.
    """
ndvi_s = 0.2
ndvi_n = 0.5

def pv_calc(ndvi, ndvi_s, ndvi_n):
  pv = (ndvi - ndvi_s) / (ndvi_n - ndvi_s) ** 2
  return pv
    """
    Calculate Proportional Vegetation
    """
location = 'LC08_L1TP_012031_20170614_20170628_01_T1_B10.TIF'
tirs = tif2array(location)
location = 'LC08_L1TP_012031_20170614_20170628_01_T1_B4.TIF'
red = tif2array(location)
location = 'LC08_L1TP_012031_20170614_20170628_01_T1_B5.TIF'
nir = tif2array(location)

def lst_calc(location):
  #Get files into arrays
  location = 'LC08_L1TP_012031_20170614_20170628_01_T1_B10.TIF'
  tirs = tif2array(location)
  location = 'LC08_L1TP_012031_20170614_20170628_01_T1_B4.TIF'
  red = tif2array(location)
  location = 'LC08_L1TP_012031_20170614_20170628_01_T1_B5.TIF'
  nir = tif2array(location)
  #get metadata constants
  meta_text = '/Users/cristinalogg/Desktop/LC08_L1TP_012031_20170614_20170628_01_T1/LC08_L1TP_012031_20170614_20170628_01_T1_MTL.txt'
  Band10Meta = retrieve_meta(meta_text)
  var_list =   Band10Meta

  ndvi = ndvi_calc(red, nir)
  rad = rad_calc(tirs, var_list)
  bt = bt_calc(rad, var_list)
  pv = pv_calc(ndvi, ndvi_s, ndvi_n)
  emis = emissivity_calc(pv, ndvi)

  wave = 10.8E-06
  # PLANCK'S CONSTANT
  h = 6.626e-34
  # SPEED OF LIGHT
  c = 2.998e8
  # BOLTZMANN's CONSTANT
  s = 1.38e-23
  p = h * c / s
  lst_filter = bt / (1 + (wave * bt / p) * np.log(emis))
  return lst_filter

    """
    #invoke functions in here
    Calculate Estimate of Land Surface Temperature.
    Your output should
    ---
    Note that this should take as its input ONLY the location
    of a directory in your file system. That means it will have
    to call your other functions. It should:
    1. Define necessary constants
    2. Read in appropriate tifs (using tif2array)
    3. Retrieve needed variables from metadata (retrieve_meta)
    4. Calculate ndvi, rad, bt, pv, emis using appropriate functions
    5. Calculate land surface temperature and return it.
    Your LST function may return strips of low-values around the raster...
    This is a processing artifact that you're not expected to account for.
    Nothing to worry about!
    """
```

Use these functions to generate an Normalized Difference Vegetation Index and a Land Surface Temperature Estimate for your downloaded Landsat data.

## Remove Clouds

Your Landsat data contains another band, whose filename ends with `_BQA.tif`. this is the so-called 'quality assessment band', which contains estimates of where there are clouds in our image. You'll need to read this `tif` in: try using your new `tif2array` function!

According to the [USGS Landsat documentation](https://landsat.usgs.gov/collectionqualityband), these values are where we can be highly confident that the image is clear and, additionally, where there are clouds and cloud shadows:

| Attribute               | Pixel Value                                                                                    |
|-------------------------|------------------------------------------------------------------------------------------------|
| Clear                   | 2720, 2724, 2728, 2732                                                                         |
| Cloud Confidence - High | 2800, 2804, 2808, 2812, 6896, 6900, 6904, 6908                                                 |
| Cloud Shadow - High     | 2976, 2980, 2984, 2988, 3008, 3012, 3016, 3020, 7072, 7076, 7080, 7084, 7104, 7108, 7112, 7116 |

Write a function that reclassifies an input Numpy array based on values stored in the BQA. The function should reclassify input data in such a way that pixels, *except for those that are clear* (for example, 2720), are assigned a value of `nan`. Use the `emissivity_calc` function as a model! We're doing something similar here! Your code will look like this:

```python
#def cloud_filter(array, bqa):
#    array_dest = array.copy()
#    array_dest[np.where((bqa != <a certain value>) & (bqa != <another certain value>)) ] = 'nan'
#    return array_dest
```

You should simply be able to revise the above function, making your criteria test for `bqa` values not equal to 2720, 2724, 2728, 2732.

```python
location = 'LC08_L1TP_012031_20170614_20170628_01_T1_BQA.TIF'
array = tif2array(location)
print(array)

def cloud_filter(array, bqa):
  array_dest = array.copy()
  array_dest2 = array_dest[np.where((bqa != 2720) & (bqa != 2724) & (bqa != 2728) & (bqa != 2732)) ] = 'nan'
  return array_dest2
    """
    Filters out clouds and cloud shadows using values of BQA.
    """
```

## Write Your Filtered Arrays as `.tifs`

You should now be able to write your NDVI and LST arrays as GeoTIFFs. For example, to write your filtered LST to a `tif` consistent with the naming convention we've requested, you would write this code (assuming you're storing your LST in a variable called `lst_filter`).

```python
tirs_path = os.path.join(DATA, '/Users/cristinalogg/Desktop/LC08_L1TP_012031_20170614_20170628_01_T1/LC08_L1TP_012031_20170614_20170628_01_T1_B10.TIF')
out_path = os.path.join(DATA, 'Logg_ndvi_20170614.tif')
array2tif(tirs_path, out_path, ndvi_calc(red, nir))

tirs_path = os.path.join(DATA, '/Users/cristinalogg/Desktop/LC08_L1TP_012031_20170614_20170628_01_T1/LC08_L1TP_012031_20170614_20170628_01_T1_BQA.TIF')
out_path = os.path.join(DATA, 'Logg_lst_20170614.tif')
array2tif(tirs_path, out_path, lst_calc(tirs_path))
```

The reason you have to specify the `tirs_path` is that GDAL looks to another raster file to obtain dimensions, etc. We could use any of our input rasters - the TIRS band was chosen somewhat arbitrarily.

Once you've written these, you should compress each of them into a zip file - two separate ZIP files! This is to ensure that the files come in under Stellar's file submission size limit. Name sure they are named correctly e.g., `yourlastname_ndvi_imagerydate.tif`, where `yourlastname` is your last name and `imagerydate` is the date the imagery was captured reported in the format `YYYYMMDD`.
