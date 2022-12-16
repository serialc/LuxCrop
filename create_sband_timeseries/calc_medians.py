from qgis.core import (
    QgsVectorLayer,
    QgsApplication
)
import qgis.utils
import os

# path variables
parcels_path = 'data/parcels/belgium_extract.shp'
sat_imgs_path = 'data/sat/'


# Loading the vector file
parcels = QgsVectorLayer(parcels_path, "belgium_extract", "ogr")

# checking it's loaded correctly
if parcels.isValid():
    print("Layer loaded successfully")
else:
    print("Layer failed to load!")

for sat_file_name in os.listdir(sat_imgs_path):
    # load sat img
    sat = QgsRasterLayer(sat_imgs_path + sat_file_name, sat_file_name")


exit()

# iterate through the features/rows of attribugte table
features = parcels.getFeatures()
for f in features:
    print("Feature ID: ", f.id())

    # want to select one feature
    print(f)


