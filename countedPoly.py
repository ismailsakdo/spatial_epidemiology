from qgis.core import QgsProject, QgsVectorLayer, QgsVectorFileWriter

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

# Filter the point layer for Week 1
expression = "\"Week\" = 1"
point_layer.setSubsetString(expression)

# Count points within each polygon
counts = {}
for polygon_feat in polygon_layer.getFeatures():
    polygon_id = polygon_feat.id()
    polygon_geom = polygon_feat.geometry()
    count = 0
    for point_feat in point_layer.getFeatures():
        point_geom = point_feat.geometry()
        if polygon_geom.contains(point_geom):
            count += 1
    counts[polygon_id] = count

# Create a temporary shapefile for the counts
counted_polygon_file = '/Users/ismailsa/Downloads/0.AaaaGIS/SabahNew/dataCase/countedPolygons.shp'
QgsVectorFileWriter.writeAsVectorFormat(
    polygon_layer,
    counted_polygon_file,
    'UTF-8',
    polygon_layer.crs(),
    'ESRI Shapefile'
)

# Load the counted polygon layer
counted_polygon_layer = QgsVectorLayer(counted_polygon_file, 'Counted Polygons', 'ogr')
if not counted_polygon_layer.isValid():
    print('Failed to load counted polygon layer:', counted_polygon_layer.error().message())

# Add the counted polygon layer to the project
QgsProject.instance().addMapLayer(counted_polygon_layer)

# Update the CaseWeek1 attribute with the counts
field_name = 'CaseW1'
counted_polygon_layer.startEditing()
counted_polygon_layer.addAttribute(QgsField(field_name, QVariant.Int))
for polygon_feat in counted_polygon_layer.getFeatures():
    polygon_id = polygon_feat.id()
    count = counts.get(polygon_id, 0)
    counted_polygon_layer.changeAttributeValue(polygon_id, counted_polygon_layer.fields().indexFromName(field_name), count)
counted_polygon_layer.commitChanges()
