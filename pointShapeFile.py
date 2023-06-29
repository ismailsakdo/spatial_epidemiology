from qgis.core import (
    QgsProject,
    QgsPointXY,
    QgsVectorLayer,
    QgsField,
    QgsGeometry,
    QgsFeature,
    QgsCoordinateReferenceSystem,
    QgsVectorFileWriter
)

from qgis.PyQt.QtCore import QVariant
from qgis.utils import iface
import csv

# Specify the path to the CSV file
csv_file_path = "/Users/ismailsa/Downloads/0.AaaaGIS/SabahNew/dataCase/dummyCase1.csv"

# Create a new point vector layer
layer_name = "CSV Points"
crs = QgsCoordinateReferenceSystem("EPSG:4326")  # Assuming WGS84 coordinates

# Read the CSV file and add features to the layer
with open(csv_file_path, "r") as file:
    csv_data = csv.reader(file)
    header = next(csv_data)  # Read and store the header row

    # Create QgsField objects for the additional columns
    additional_fields = [QgsField(header[i], QVariant.String) for i in range(3, len(header))]

    # Create the layer with all necessary fields
    fields = [
        QgsField("ID", QVariant.Int),
        QgsField("X", QVariant.Double),
        QgsField("Y", QVariant.Double),
        QgsField("Gender", QVariant.String),
        QgsField("Year", QVariant.Int),
        QgsField("Week", QVariant.Int),
        QgsField("Child", QVariant.Int),
        QgsField("Income", QVariant.String),
        QgsField("House", QVariant.String),
        QgsField("Education", QVariant.String)
    ] + additional_fields

    layer = QgsVectorLayer("Point?crs={}".format(crs.toWkt()), layer_name, "memory")
    provider = layer.dataProvider()
    provider.addAttributes(fields)
    layer.updateFields()

    for row in csv_data:
        id = int(row[0])
        x, y = float(row[1]), float(row[2])
        gender = row[3]
        year = int(row[4])
        week = int(row[5])
        child = int(row[6])
        income = row[7]
        house = row[8]
        education = row[9]

        point = QgsPointXY(x, y)
        geom = QgsGeometry.fromPointXY(point)
        feature = QgsFeature()
        feature.setGeometry(geom)

        # Extract the additional column values and add them as attributes
        additional_values = [row[i] for i in range(3, len(row))]
        attributes = [id, x, y, gender, year, week, child, income, house, education] + additional_values
        feature.setAttributes(attributes)
        provider.addFeature(feature)

# Add the layer to the map
QgsProject.instance().addMapLayer(layer)

# Filter the points layer by "Week" equal to 4
expr = QgsExpression("\"Week\" = 4")
request = QgsFeatureRequest(expr)
filtered_features = []
for feature in layer.getFeatures(request):
    filtered_features.append(feature)

# Create a new layer with filtered features
filtered_layer = QgsVectorLayer("Point?crs={}".format(crs.toWkt()), "Filtered Points", "memory")
filtered_provider = filtered_layer.dataProvider()
filtered_provider.addAttributes(fields)
filtered_layer.updateFields()

for feature in filtered_features:
    filtered_provider.addFeature(feature)

# Add the filtered layer to the map
QgsProject.instance().addMapLayer(filtered_layer)

# Load the shapefile polygon layer
shapefilePoly_path = '/Users/ismailsa/Downloads/0.AaaaGIS/SabahNew/dataCase/sabahDummy.shp'
shapefilePoly_layer_name = 'Shapefile'
shapefilePoly_provider_type = 'ogr'
shapefilePoly_layer = QgsVectorLayer(shapefilePoly_path, shapefilePoly_layer_name, shapefilePoly_provider_type)

# Check if the shapefile layer was loaded successfully
if not shapefilePoly_layer.isValid():
    print("Failed to load the shapefile layer!")
    exit()

# Add the shapefile layer to the QGIS workspace
iface.addVectorLayer(shapefilePoly_path, shapefilePoly_layer_name, shapefilePoly_provider_type)

# Perform point in polygon analysis
processing.run("qgis:countpointsinpolygon", {
    'POINTS': filtered_layer,
    'POLYGONS': shapefilePoly_layer,
    'FIELD': 'Week4',
    'OUTPUT': '/Users/ismailsa/Downloads/0.AaaaGIS/SabahNew/dataCase/caseFile.shp'
})

# Load the resulting case file as a vector layer
case_file_path = '/Users/ismailsa/Downloads/0.AaaaGIS/SabahNew/dataCase/caseFile.shp'
case_file_layer = QgsVectorLayer(case_file_path, 'Case File', 'ogr')

if not case_file_layer.isValid():
    print("Failed to load the case file layer!")
    exit()

# Add the case file layer to the map
QgsProject.instance().addMapLayer(case_file_layer)

# Remove the temporary layers
QgsProject.instance().removeMapLayer(layer)
QgsProject.instance().removeMapLayer(filtered_layer)
QgsProject.instance().removeMapLayer(shapefilePoly_layer)
