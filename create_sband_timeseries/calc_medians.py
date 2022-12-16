from qgis.core import (
    QgsApplication,
    QgsVectorLayer,
    QgsRasterLayer
)
import qgis.utils
import os
#import processing
from pathlib import Path

# setup QGIS so we can display data
qgs = QgsApplication([], True)
QgsApplication.setPrefixPath("/usr/bin/qgis", True)
QgsApplication.initQgis()

# path variables
parcels_path = 'data/parcels/belgium_extract.shp'
sat_imgs_path = 'data/sat/'

# Loading the vector file
parcels = QgsVectorLayer(parcels_path, "belgium_sample", "ogr")

# checking it's loaded correctly
if parcels.isValid():
    print("Layer loaded successfully")
else:
    print("Layer failed to load!")

# loading 
for sat_file_name in os.listdir(sat_imgs_path):
    # load sat img
    sat = QgsRasterLayer(sat_imgs_path + sat_file_name, Path(sat_file_name).stem)

    # checking it's loaded correctly
    if sat.isValid():
        print("Raster " + sat_file_name + " loaded successfully")
    else:
        print("Raster failed to load!")

    print("Sat imagery dimensions: ", sat.width(), sat.height())
    print(sat.rasterType())


    # iterate through the features/rows of attribugte table
    features = parcels.getFeatures()
    for f in features:
        print("Feature ID: ", f.id())

        # want to select one feature
        print(f)

        parameters = {'INPUT': sat,
        'MASK': f,
        'NODATA': -9999,
        'ALPHA_BAND': False,
        'CROP_TO_CUTLINE': True,
        'KEEP_RESOLUTION': True,
        'OPTIONS': None,
        'DATA_TYPE': 0,
        'OUTPUT': 'temp'}

        #processing.runAndLoadResults('gdal:cliprasterbymasklayer', parameters)


    print("STOPPING after one sat for now")
    exit()

qgs.exitQgis()
