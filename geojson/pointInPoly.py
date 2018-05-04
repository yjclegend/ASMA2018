import json
from shapely.geometry import shape, Point
# depending on your version, use: from shapely.geometry import shape, Point

# load GeoJSON file containing sectors
with open('SA4_2016_AUST.json') as f:
    js = json.load(f)

# construct point based on lon/lat returned by geocoder
point = Point(-122.7924463, 45.4519896)

# check each polygon to see if it contains the point
for feature in js['features']:
    polygon = shape(feature['geometry'])
    if polygon.contains(point):
        print('Found containing polygon:', feature)