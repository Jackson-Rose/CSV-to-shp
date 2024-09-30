import geopandas
import pandas as pd
import folium
csv_file = input('Enter csv file name: ')
file_name = input('Enter desired file name for shapefile: ')
if csv_file[len(csv_file)-4:len(csv_file)] != '.csv':
    print('Please enter a file name that ends in ".csv"')
    exit()
xy_table = pd.read_csv(csv_file)
xy_table.head()
# creating a list of coordinates and displaying them in a new column called 'coordinates'
xy_table['coordinates'] = xy_table[['LONGITUD', 'LATITUD']].values.tolist()
xy_table.head()
from shapely.geometry import Point
# converting each coordinate pair into a Shapely Point object
xy_table['coordinates'] = xy_table['coordinates'].apply(Point)
xy_table.head()
# converting to GeoDataFrame, using our coordinates column as the geometry column
stations = geopandas.GeoDataFrame(xy_table, geometry = 'coordinates')
stations.plot()
# creating a Folium map centered around the average latitude and longitude of all coordinate pairs
map = folium.Map(location=[stations.LATITUD.mean(), stations.LONGITUD.mean()], zoom_start=7)
# creating a Folium GeoJSON layer
points = folium.features.GeoJson(stations.to_json())
# Adding the GeoJSON points to the Folium map
map.add_child(points)
# setting CRS
stations = stations.set_crs('epsg:4326')
stations_epsg3117 = stations.to_crs('EPSG:3117')
stations.to_file(file_name)
