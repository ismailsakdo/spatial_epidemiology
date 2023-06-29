from qgis.core import QgsVectorLayer, QgsField, QgsFeature, QgsGeometry
from qgis.PyQt.QtCore import QVariant
from qgis.utils import iface

# Path to the shapefile
shapefile_path = '/Users/ismailsa/Downloads/0.AaaaGIS/SabahNew/dataCase/sabahDummy.shp'
shapefile_layer_name = 'Shapefile'
shapefile_provider_type = 'ogr'

# Load the shapefile
shapefile_layer = QgsVectorLayer(shapefile_path, shapefile_layer_name, shapefile_provider_type)

# Check if the shapefile layer was loaded successfully
if not shapefile_layer.isValid():
    print("Failed to load the shapefile layer!")
    exit()

# Add the shapefile layer to the QGIS workspace
iface.addVectorLayer(shapefile_path, shapefile_layer_name, shapefile_provider_type)

# Set the active layer in the QGIS GUI to the shapefile layer
iface.setActiveLayer(shapefile_layer)

# Zoom to the extent of the shapefile layer
iface.zoomToActiveLayer()

#=======
