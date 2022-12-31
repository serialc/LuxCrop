# LuxCrop
A project based on [EuroCrops](https://www.eurocrops.tum.de/index.html), aiming to identify crop types in Luxembourg from satellite imagery.

## Pipeline

- Apply zonal statistics to parcels to get the median band value for each satellite measurement over the year.
  - So if we have monthly (12) satellite images, with 13 bands of data, with 100 parcels, we can create a 'data-cube' of 12x13x10=1560 values.
  - We should convert this to HDF format for compatibility with EuroCrops.
- Classify temporal trends according to defined clusters of interest with training data.
- Apply model to study area (test data).

### Calculating parcel medians

Requires QGIS to be installed, or at least PyQGIS.

*Currently this just runs zonal statistics - still needs to repackage to HDF format*

Download the script and create the appropriate folders:

1. Make sure you have your parcels file in the right location (data/parcels/my_parcels.shp)
2. Make sure you have your satellite imagery in the right location (data/sat/)
3. Update the end of the the calc_median.py file to point to the parcels file above (1) and satellites path (2)

Run the script.

The data will be placed in a copy of the shapefile (named \*\_zonalstats.gpkg) with all the info in the attributes table.
We use a gpkg to store the data as it's possible to have more descriptive field names. Shape files are limited to 10 characters.
The columns have the form [sat image file name]\_[band number]\_median


## Resources

EuroCrops
- [The project website that LuxCrop expands on and aims to contribute to](https://www.eurocrops.tum.de/) ([Github](https://github.com/maja601/EuroCrops))
- [Sentinel 2 bands description](https://gisgeography.com/sentinel-2-bands-combinations/)
- [M. Schneider replication](https://github.com/maja601/RC2020-psetae)
- [PyTorch Satellite Image Time Series Classification PSE & TSA](https://github.com/VSainteuf/pytorch-psetae)
- [Presentation by M. Schneider on the project](https://eurogeographics.org/wp-content/uploads/2022/02/4.-EuroCrops_GeodataDiscoverability28042022-Maya-Schneider.pdf)

Methodology/Coding
- [Introduction to Earth Engine Python API](https://developers.google.com/earth-engine/tutorials/community/intro-to-python-api)

Sentinel data download
- [SNAP](https://step.esa.int/main/download/snap-download/) allows easier satellite imagery download and Python integration (with the SNAPISTA wrapper)
