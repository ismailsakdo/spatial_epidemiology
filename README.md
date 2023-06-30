# Spatial Epidemiology
Spatial Epidemiology Formula and Coding

Google Sheet Formula
1) Formula 1: =IF(A1=0, "Male", IF(A1=1, "Female", ""))
2) Formula 2: =IF(A1=0, "Terrace", IF(A1=1, "Village House", IF(A1=2, "Others", "")))
3) Formula 3: =CHOOSE(RANDBETWEEN(1,3), "Terrace", "Village House", "Others")

Python:
/Users/ismailsa/Downloads/0.AaaaGIS/SabahNew/dataCase/

STEP:
1) [Insert ShapeFile](https://github.com/ismailsakdo/spatial_epidemiology/blob/main/insertShapeFile.py)
2) [Insert CSV as XY point data](https://github.com/ismailsakdo/spatial_epidemiology/blob/main/insertCSVasVector.py)
3) [Insert CSV as 10 Column and Save the Shape](https://github.com/ismailsakdo/spatial_epidemiology/blob/main/insertCSV10colSHPsave.py)
4) [Insert Point and Poly, Then Save the Point as Shape](https://github.com/ismailsakdo/spatial_epidemiology/blob/main/insertPointPolygon.py)
5) [Insert Point Data into the Polygon and Count Point in Polygon in Week 4](https://github.com/ismailsakdo/spatial_epidemiology/blob/main/insertPointPolygon.py)
6) [Count Point Polygon and Safe as CaseFile](https://github.com/ismailsakdo/spatial_epidemiology/blob/main/countPointPolygonSave.py)
7) [Final Code Day1](https://github.com/ismailsakdo/spatial_epidemiology/blob/main/pointINpolygonClose.py)

## Day 2
1) Call the shapefile and filter the data [LINK](https://github.com/ismailsakdo/spatial_epidemiology/blob/main/importFilter.py)
2) Filter by OR [LINK](https://github.com/ismailsakdo/spatial_epidemiology/blob/main/filterBYor.py)
3) Filter by multiple Week [Link](https://github.com/ismailsakdo/spatial_epidemiology/blob/main/filterWeek1till4.py)
4) Counted Poly Week 1 and safe as new Counted Poly [LINK](https://github.com/ismailsakdo/spatial_epidemiology/blob/main/countedPoly.py)
