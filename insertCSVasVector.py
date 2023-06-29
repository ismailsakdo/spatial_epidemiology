from qgis.core import (
    QgsProject,
    QgsPointXY,
    QgsVectorLayer,
    QgsField,
    QgsGeometry,
    QgsFeature,
    QgsCoordinateReferenceSystem
)
import csv

# Specify the path to the CSV file
csv_file_path = "/Users/Name/Folder1/0.AaaaGIS/dummyCase1.csv"

# Create a new point vector layer
layer_name = "CSV Points"
crs = QgsCoordinateReferenceSystem("EPSG:4326")  # Assuming WGS84 coordinates

fields = [
    QgsField("X", QVariant.Double),
    QgsField("Y", QVariant.Double)
]

layer = QgsVectorLayer("Point?crs={}".format(crs.toWkt()), layer_name, "memory")
provider = layer.dataProvider()
provider.addAttributes(fields)
layer.updateFields()

# Read the CSV file and add features to the layer
with open(csv_file_path, "r") as file:
    csv_data = csv.reader(file)
    next(csv_data)  # Skip header row if it exists

    for row in csv_data:
        x, y = float(row[1]), float(row[2])
        point = QgsPointXY(x, y)
        geom = QgsGeometry.fromPointXY(point)
        feature = QgsFeature()
        feature.setGeometry(geom)
        feature.setAttributes([x, y])
        provider.addFeature(feature)

# Add the layer to the map
QgsProject.instance().addMapLayer(layer)
