from qgis.core import QgsProject, QgsVectorLayer

# Set the paths to your shapefiles
polygon_file = '/Users/ismailsa/Downloads/0.AaaaGIS/SabahNew/dataCase/caseFile.shp'
point_file = '/Users/ismailsa/Downloads/0.AaaaGIS/SabahNew/dataCase/dummyCase1.shp'

# Load the polygon layer
polygon_layer = QgsVectorLayer(polygon_file, 'Polygon Layer', 'ogr')
if not polygon_layer.isValid():
    print('Failed to load polygon layer:', polygon_layer.error().message())

# Load the point layer
point_layer = QgsVectorLayer(point_file, 'Point Layer', 'ogr')
if not point_layer.isValid():
    print('Failed to load point layer:', point_layer.error().message())

# Add the layers to the project
QgsProject.instance().addMapLayer(polygon_layer)
QgsProject.instance().addMapLayer(point_layer)

# Filter the point layer for Week 1 to Week 4
expression = "\"Week\" = 1"
point_layer.setSubsetString(expression)
