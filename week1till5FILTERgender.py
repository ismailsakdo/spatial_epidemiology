from qgis.core import QgsProject, QgsVectorLayer, QgsVectorFileWriter, QgsField

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

# Create a temporary shapefile for the counts
counted_polygon_file = '/Users/ismailsa/Downloads/0.AaaaGIS/SabahNew/dataCase/countedPolygon.shp'
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

# Filter the point layer for Gender = Male
expression = "\"Gender\" = 'Male'"
point_layer.setSubsetString(expression)

# Calculate counts for each week separately
week_attributes = ['CaseW1', 'CaseW2', 'CaseW3']  # Attribute names for each week
for week in range(1, 4):
    # Filter the point layer for the current week
    expression = "\"Week\" = {}".format(week)
    point_layer.setSubsetString(expression)

    # Count points within each polygon for the current week
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

    # Update the attribute for the current week
    field_name = week_attributes[week - 1]
    counted_polygon_layer.startEditing()
    if not counted_polygon_layer.fields().indexFromName(field_name) >= 0:
        # Add attribute field if it doesn't exist
        attribute = QgsField(field_name, QVariant.Int)
        counted_polygon_layer.addAttribute(attribute)
    for polygon_feat in counted_polygon_layer.getFeatures():
        polygon_id = polygon_feat.id()
        count = counts.get(polygon_id, 0)
        counted_polygon_layer.changeAttributeValue(polygon_id, counted_polygon_layer.fields().indexFromName(field_name), count)
    counted_polygon_layer.commitChanges()
