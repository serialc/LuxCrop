# load the python modules
import os
from pathlib import Path

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

# package our main algorithm in a wrapper
def loadQgisWrapper(pfn, satpath):
    # setup QGIS so we can display data
    qgs = QgsApplication([], True)
    QgsApplication.setPrefixPath("/usr/bin/qgis", True)
    QgsApplication.initQgis()

    calculateZonalMedians(pfn, satpath)

    qgs.exitQgis()

def calculateZonalMedians(parcels_fullpathname, satpath):

    parcels_fp = str(Path(parcels_fullpathname).parent) + '/'
    parcels_fname = Path(parcels_fullpathname).stem

    # Loading the vector file
    parcels = QgsVectorLayer(parcels_fullpathname, None, "ogr")

    # create a copy in which we will store median values
    #p2_fullpathname = parcels_fp + parcels_fname + '_zonalstats.shp'
    p2_fullpathname = parcels_fp + parcels_fname + '_zonalstats.gpkg'

    QgsVectorFileWriter.writeAsVectorFormat(parcels, p2_fullpathname, "UTF-8", parcels.crs(), "GPKG")
    #QgsVectorFileWriter.writeAsVectorFormat(parcels, p2_fullpathname, 'utf-8', parcels.crs(), 'ESRI Shapefile')

    # use this copy to append zonal statistics to
    p2 = QgsVectorLayer(p2_fullpathname, None, 'ogr')

    # checking it's loaded correctly
    if p2.isValid():
        print("Parcels layer loaded successfully. Ignore deprecation warning above (for now).\n")
    else:
        exit("Failed to load parcels layer!")

    # loading 
    satimg = 1
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
            print("Success!")
        else:
            print("Failure - skipping!")
            continue

        # we want a multiband raster
        if sat.rasterType() != 2:
            print("Raster is not multiband! Skipping.")

        # ok, looks valid - let's show some basic info
        print("Sat imagery dimensions are: ", sat.width(), sat.height(), " with band count of ", sat.bandCount())

        # go through each band for this sat imagery
        for bn in range(1, sat.bandCount() + 1):
            # column names have a 8char max
            # appends columns to data
            #QgsZonalStatistics(p2, sat, str(satimg) + '_' + str(bn), rasterBand=bn, stats=QgsZonalStatistics.Median).calculateStatistics(None)
            QgsZonalStatistics(p2, sat, str(rfname) + '_' + str(bn) + "_", rasterBand=bn, stats=QgsZonalStatistics.Median).calculateStatistics(None)

        # count the sat imagery index
        satimg +=1
        print("")

# Start the process
parcels_filepath = 'data/parcels/belgium_extract.shp'
sat_imgs_path = 'data/sat/'

loadQgisWrapper(parcels_filepath, sat_imgs_path)

