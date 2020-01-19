"""
Map Examples using Python and Folium
------------------------------------

Written by Elliot Palmer, 2020-01-19

From Folium Docs:
folium builds on the data wrangling strengths of the Python ecosystem and 
the mapping strengths of the Leaflet.js library. Manipulate your data in Python, 
then visualize it in a Leaflet map via folium.

Github: https://github.com/python-visualization/folium
Docs: https://python-visualization.github.io/folium/
Examples: https://nbviewer.jupyter.org/github/python-visualization/folium/tree/master/examples/
"""

# Import Libraries
import folium
import os
import json
import requests
import pandas as pd
from folium.plugins import HeatMap
import numpy as np

# Link to Zipcode GeoJSON Files compiled on Github 
# TODO: Link to the true up to date census files
zip_url = 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/oh_ohio_zip_codes_geo.min.json'

# Return the data
print('Getting Zip Code Shapefile Data...')
response = requests.get(zip_url)
zips = response.json()

# Create a copy for manipulation
tmp = zips.copy()

# Get and Manipulate Data
# TODO: add connection to database file

# Read in Datasets
print("Loading and Manipulating Data...")
df_zip = pd.read_csv('./data/zipyear.csv')
df_jobs = pd.read_csv('./data/jobs.csv')

# Add Metrics
df_zip['conv'] = df_zip['sold_jobs'] / df_zip['jobs']
df_zip['atv'] = df_zip['revenue'] / df_zip['sold_jobs']

# Filter Data
filter_conv = df_zip[df_zip['jobs'] > 100]

# Remove NAs from dataset
df_jobs = df_jobs.dropna()

# Create Array for HeatMap Plugin
# Note: Can be 2d or 3d, where the first 2 elements are lat, lon 
# and the 3rd element is the variable that weights the intensity
heatmap_array = np.array(df_jobs[['lat','lon','invoice_total']]).tolist()

# Filter the Zip Codes to create based on the zip dataframe
print("Updating GeoJSON for Mapping...")
geozips = []
for i in range(len(tmp['features'])):
    if tmp['features'][i]['properties']['ZCTA5CE10'] in list(df_zip['zip']):
        geozips.append(tmp['features'][i])

# Create a new GeoJSON file from the filtered data
new_json = dict.fromkeys(['type','features'])
new_json['type'] = 'FeatureCollection'
new_json['features'] = geozips

# Write the new JSON file to disk
open("updated-file.json","w").write(
    json.dumps(new_json, sort_keys=True, indent=4, separators=(',',": "))
)

# Name the file to variable
oh_geo = r'updated-file.json'

# MAPPING ... FINALLY

# Create the map object
print("Creating Map Layers...")
map = folium.Map(
    location=[40.0384605,-83.0424027], 
    zoom_start=11, 
    tiles='cartodbpositron'
)

# Heat Map Layer
HeatMap(
    heatmap_array,
    name='Heat Map', 
    radius=5, 
    max_val=1000, 
    blur=4, 
    show=False,
    gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'}
).add_to(map)

# Zip Boundaries w/o Fill based on a variable
folium.Choropleth(
    name='Zip Boundaries',
    geo_data=oh_geo,
    fill_opacity=0.05,
    line_opacity=.5,
    fill_color=None,
    key_on = 'feature.properties.ZCTA5CE10',
).add_to(map)

# Function for Creating Zip Layers
def zip_layer(name="Layer", geo_data=oh_geo, 
    key_on="feature.properties.ZCTA5CE10",z_data=None, z=None, fill_color="YlGn"):

    layer = folium.Choropleth(
        name=name,
        geo_data=geo_data,
        fill_opacity=0.7,
        line_opacity=.1,
        key_on = key_on,
        data=z_data,
        columns=['zip',z],
        fill_color=fill_color,
    )

    return layer

# Zip Fill based on Conversion
zip_layer(name="Conversion", z_data=filter_conv, z='conv').add_to(map)

# Zip Fill based on Revenue
zip_layer(name="Revenue", z_data=df_zip, z='revenue').add_to(map)

# Zip Fill based on Average Ticket
zip_layer(name="Average Ticket", z_data=df_zip, z='atv').add_to(map)

# Add Controls for showing and removing different layers
folium.LayerControl(collapsed=False).add_to(map)

# Output file as HTML File
print("Creating Map File...")
map.save(outfile='./output/test_map.html')

print("Map Complete!")