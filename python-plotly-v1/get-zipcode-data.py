import os
import json
import requests

#https://github.com/OpenDataDE/State-zip-code-GeoJSON

zip_url = 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/oh_ohio_zip_codes_geo.min.json'

print('Getting Zip Code Shapefile Data...')
response = requests.get(zip_url)
zips = response.json()

print('Writing Data to Folder: geoJSON')
open("./geoJSON/ohioZipGeoJSON.json","w").write(
    json.dumps(zips, sort_keys=True, indent=4, separators=(',',": "))
)