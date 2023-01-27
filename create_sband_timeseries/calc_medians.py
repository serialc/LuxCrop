# load the python modules
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import h5py

# load the QGIS modules
from qgis.core import (
    QgsApplication,
    QgsVectorLayer,
    QgsProject,
    QgsRasterLayer,
    QgsVectorFileWriter
)
from qgis.analysis import QgsZonalStatistics
import qgis.utils

# Read the command line arguments for the source files
if len(sys.argv) != 3:
    print("Use in the following manner:\npython3 calc_medians.py path/to/parcels_vector_file path/to/sat/imagery/")
    print("Example:\npython3 calc_medians.py data/parcels/belgium_extract.shp data/sat/")
    exit()
else:
    parcels_filepath = sys.argv[1]
    sat_imgs_path = sys.argv[2]
    # add slash for folder if there isn't one
    if sat_imgs_path[-1] != '/':
        sat_imgs_path += '/'
    print("-> Loading parcels vector file from " + parcels_filepath)
    print("-> Loading satellite imagery from " + sat_imgs_path)


# package our main algorithm in a wrapper
def loadQgisWrapper(pfn, satpath): # setup QGIS so we can display data
    qgs = QgsApplication([], True)
    QgsApplication.setPrefixPath("/usr/bin/qgis", True)
    QgsApplication.initQgis()

    calculateZonalMedians(pfn, satpath)

    qgs.exitQgis()

def calculateZonalMedians(parcels_fullpathname, satpath):

    # file path and file name of vector/parcels file
    parcels_fp = str(Path(parcels_fullpathname).parent) + '/'
    parcels_fname = Path(parcels_fullpathname).stem
    parcels_ftype = Path(parcels_fullpathname).suffix.lower()

    # Loading the vector file (of any type)
    parcels = QgsVectorLayer(parcels_fullpathname, None, "ogr")

    # create a copy in which we will store median values - need a gpkg to store descriptive field names
    p2_fullpathname = parcels_fp + parcels_fname + '_zonalstats.gpkg'

    # save options, geopackage is default data type - which is good as it allows longer field names
    save_options = QgsVectorFileWriter.SaveVectorOptions()
    tran_context = QgsProject.instance().transformContext()
    QgsVectorFileWriter.writeAsVectorFormatV3(parcels, p2_fullpathname, tran_context, save_options)

    # use this copy to append zonal statistics to
    p2 = QgsVectorLayer(p2_fullpathname, None, 'ogr')

    # checking it's loaded correctly
    if p2.isValid():
        print("Parcels layer loaded successfully.")
    else:
        exit("Failed to load parcels layer " + parcels_fullpathname)


    # load each satellite/raster and get median for each parcel for each band
    sat_dates_list = []
    for sfn in os.listdir(satpath):

        # get extension in lowercase
        rftype = Path(sfn).suffix.lower()
        rfname = Path(sfn).stem
        rfp = Path(sfn).parent

        # check this is a *.tif
        if rftype != '.tif':
            print("Skipping " + sfn + " as it's not a *.tif")
            continue
        else:
            print("Trying to load " + sfn + "... ", end="")

        # load sat img
        sat = QgsRasterLayer(satpath + sfn, sfn)

        # checking it's loaded correctly
        if sat.isValid():
            print("It is valid.", end=' ')
        else:
            print("Failure - skipping!")
            continue

        # add to list - convert date to int 
        sat_dates_list.append(int(rfname.replace('-','')))

        # we want a multiband raster
        if sat.rasterType() != 2:
            print("But the raster is not multiband! Skipping.")
            continue

        # ok, looks valid - let's show some basic info
        print("Sat imagery dimensions are: ", sat.width(), sat.height(), " with band count of ", sat.bandCount())

        # go through each band for this sat imagery
        #for bn in range(1, sat.bandCount() + 1):
        # only want the 13 bands - ignore QA10, QA20, QA60
        for bn in range(1, 14):
            # appends sat median for each parcel to a column named after the raster layer (should be the date)
            QgsZonalStatistics(p2, sat, str(rfname) + '_' + str(bn) + "_", rasterBand=bn, stats=QgsZonalStatistics.Median).calculateStatistics(None)

    print("Calculation of all parcel medians for all satellite images completed.")

    # get the index of the first median data row
    satimgcount = len(sat_dates_list)
    mdi = len(p2.fields()) - satimgcount*13

    # get the field names - don't currently need
    #field_names = [x.name() for x in p2.fields()]
    #sfn = [x.split('_')[0] for x in field_names[mdi:]] # not we cut off the non median data

    # for each parcel, get the 13 data points/band median for each satellite imagery
    d = []
    for f in p2.getFeatures():
        att = f.attributes()
        # get just the median attriubtes skip the original parcel data
        #matt = np.array(att[mdi:])
        matt = att[mdi:]

        # convert from 0-1 floats to 0-10,000 ints
        intmatt = [int(v * 10000) for v in matt]

        # split into groups of bands
        smatt = []
        for i in range(0, len(intmatt), 13):
            smatt.append(intmatt[i:i+13])

        # add to data list
        d.append(smatt)

    # repackage as a pandas dataframe
    # get the parcel ids
    pids = [int(f[1]) for f in p2.getFeatures()]
    df = pd.DataFrame(data=d, index=pids, columns=sat_dates_list, dtype=int)

    print(df)

    # save to HDF file 
    hdf_fn = parcels_fp + parcels_fname + '.h5'

    # method 1
    #hf = h5py.File(hdf_fn, 'w')
    #hf.create_dataset('', data=
    #hf.close()

    # method 2
    #hdf = pd.HDFStore(hdf_fn)
    #hdf.put(parcels_fname, df, format='table', data_columns=True)
    #hdf.close()

    # method 3
    #df.to_hdf(hdf_fn, key=parcels_fname);

    print("Finished")

# Start the process
loadQgisWrapper(parcels_filepath, sat_imgs_path)

