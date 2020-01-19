import folium
import os
import json
import requests
import pandas as pd
from folium.plugins import HeatMap
import numpy as np

zip_url = 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/oh_ohio_zip_codes_geo.min.json'

from urllib.request import urlopen
import json
with urlopen(zip_url) as response:
    zips = json.load(response)

tmp = zips

df = pd.read_csv('./zipyear.csv')
df['conv'] = df['sold_jobs'] / df['jobs']

forConv = df[df['jobs'] > 100]

data = pd.read_csv('./jobs.csv')

data = data.dropna()

hm = (np.array(
    data[['lat','lon','invoice_total']]
)
).tolist()

geozips = []
for i in range(len(tmp['features'])):
    if tmp['features'][i]['properties']['ZCTA5CE10'] in list(df['zip']):
        geozips.append(tmp['features'][i])

new_json = dict.fromkeys(['type','features'])
new_json['type'] = 'FeatureCollection'
new_json['features'] = geozips

open("updated-file.json","w").write(
    json.dumps(new_json, sort_keys=True, indent=4, separators=(',',": "))
)



oh_geo = r'updated-file.json'

m = folium.Map(location=[40.0384605,-83.0424027], zoom_start=11, tiles='cartodbpositron')

HeatMap(hm,name='Heat Map', radius=5, max_val=750, blur=4, show=False,
     gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'}).add_to(m)

folium.Choropleth(
    name='Zip Boundaries',
    geo_data=oh_geo,
    fill_opacity=0.05,
    line_opacity=.5,
    key_on = 'feature.properties.ZCTA5CE10',
).add_to(m)

folium.Choropleth(
    name='Conversion',
    geo_data=oh_geo,
    fill_opacity=0.7,
    line_opacity=.1,
    key_on = 'feature.properties.ZCTA5CE10',
    data=forConv,
    columns=['zip','conv'],
    fill_color="YlGn",
).add_to(m)

folium.Choropleth(
    name='Revenue',
    geo_data=oh_geo,
    fill_opacity=0.7,
    line_opacity=.1,
    key_on = 'feature.properties.ZCTA5CE10',
    data=df,
    columns=['zip','revenue'],
    fill_color="YlGn",
).add_to(m)

folium.LayerControl(collapsed=False, type='radio').add_to(m)
m.save(outfile='test_map.html')