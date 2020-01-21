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
import geopandas as gpd
import pandas as pd
import folium, branca
import fiona, requests, json

from folium.features import GeoJson, GeoJsonTooltip

# Link to Zipcode GeoJSON Files compiled on Github 
# TODO: Link to the true up to date census files

# Using geopandas to read in and parse the geoJSON
print('Getting Zip Code Shapefile Data...')
ohZips = r'./geoJSON/ohioZipGeoJSON.json'

zips = gpd.GeoDataFrame.from_features(json.load(open(ohZips)), crs=fiona.crs.from_epsg(4326))

# Create a copy for manipulation
tmp = zips.copy()

# Get and Manipulate Data
# TODO: add connection to database file

# Read in Datasets
print("Loading and Manipulating Data...")
df_zip = pd.read_csv('./data/zipyear.csv')

# Add Metrics
df_zip['conv'] = df_zip['sold_jobs'] / df_zip['jobs']
df_zip['atv'] = df_zip['revenue'] / df_zip['sold_jobs']

# Merge GeoJSON and Data Set By Zip Code
zipmerge = tmp.merge(df_zip, how="inner", left_on='ZCTA5CE10', right_on='zip')
# ^ Using the inner join allows us to filter the data "automaticall"
# zipmerge = zipmerge.to_crs({'init': 'epsg:4326'})

# MAPPING ... FINALLY

# Create the colorspace for coloring the choropleth
colormap = branca.colormap.LinearColormap(vmin=zipmerge['revenue'].quantile(0.0), 
                                        vmax=zipmerge['revenue'].quantile(1), 
                                        colors=['white','darkgreen'],
                                       caption="Zip Code Revenue")

def make_colormap(df_col, color_scheme=['white','darkgreen'], label=""):
    return branca.colormap.LinearColormap(
        vmin=df_col.quantile(0.0), 
        vmax=df_col.quantile(1), 
        colors=color_scheme,
        caption=label
    )

rev_colormap = make_colormap(zipmerge['revenue'], label="Zip Code Revenue", color_scheme=["#e0ecf4","#9ebcda","#8856a7"])
conv_colormap = make_colormap(zipmerge['conv'], label="Zip Code Conversion")

# Create the map object
print("Creating Map Layers...")
map = folium.Map(
    location=[40.0384605,-83.0424027], 
    zoom_start=11, 
    tiles='cartodbpositron'
)

tooltip=GeoJsonTooltip(
    fields=["zip", "revenue", "conv", "atv"],
    aliases=["Zip Code:", "Revenue:", "Conversion %:", "Average Ticket: "],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 1px solid black;
        border-radius: 3px;
        box-shadow: 3px;
        padding: 10px;
    """
)
tooltip2=GeoJsonTooltip(
    fields=["zip", "revenue", "conv", "atv"],
    aliases=["Zip Code:", "Revenue:", "Conversion %:", "Average Ticket: "],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 1px solid black;
        border-radius: 3px;
        box-shadow: 3px;
        padding: 10px;
    """
)

folium.GeoJson(
    zipmerge,
    name="Revenue",
    style_function=lambda x: {
        "fillColor": rev_colormap(x["properties"]["revenue"])
                        if x["properties"]["revenue"] is not None
                        else "transparent",
        "color": "transparent",
        "lineOpacity": .1,
        "fillOpacity": 0.7,
    },
    tooltip=tooltip
).add_to(map)

folium.GeoJson(
    zipmerge,
    name="Conversion",
    style_function=lambda x: {
        "fillColor": conv_colormap(x["properties"]["conv"])
                        if x["properties"]["conv"] is not None
                        else "transparent",
        "color": "transparent",
        "lineOpacity": .1,
        "fillOpacity": 0.7,
    },
    tooltip=tooltip2
).add_to(map)

# Add Controls for showing and removing different layers
folium.LayerControl(collapsed=False).add_to(map)

# Output file as HTML File
print("Creating Map File...")
map.save(outfile='./output/test_map2.html')

print("Map Complete!")
