import pandas as pd
df = pd.read_csv('jobs.csv')

filt = df[
    (df.invoice_total > 0) & 
    (df.status == 'Completed') &
    (df.completedOn > '2018-06-01')
]

import plotly.express as px
fig = px.density_mapbox(filt, lat='lat', lon='lon', z='invoice_total', radius=15,
                        center=dict(lat=40.0384605, lon=-83.0424027), zoom=8,
                        mapbox_style="open-street-map")
fig.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=-83.0424027)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.update_layout(opacity=0.5)
fig.show()

# 

from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                   dtype={"fips": str})

import plotly.graph_objects as go

fig = go.Figure(go.Choroplethmapbox(geojson=counties, ids=counties['features'], locations=df.fips, z=df.unemp,
                                    colorscale="Viridis", zmin=0, zmax=12,
                                    marker_opacity=0.5, marker_line_width=0))
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

# https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/oh_ohio_zip_codes_geo.min.json

zip_url = 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/oh_ohio_zip_codes_geo.min.json'

from urllib.request import urlopen
import json
with urlopen(zip_url) as response:
    counties = json.load(response)

len(counties['features'])

import pandas as pd

df = pd.DataFrame(
    {"fips": ["43081"],
    "unemp": [.02]}
)

import plotly.graph_objects as go

fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=df.fips, z=df.unemp,
                                    colorscale="Viridis", zmin=0, zmax=12,
                                    marker_opacity=0.5, marker_line_width=0))
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
