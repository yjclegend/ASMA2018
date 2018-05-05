import json
from shapely.geometry import shape, Point,Polygon,MultiPolygon
# depending on your version, use: from shapely.geometry import shape, Point

# load GeoJSON file containing sectors
js = None
with open('SA4_2016_AUST.json') as f:
    js = json.load(f)

#sss = js.get('type')
#print(sss)
# construct point based on lon/lat returned by geocoder
point = Point(142.7924463, -37.4519896)
feature = js['features'][0]
coors = feature['geometry']['coordinates']
print('dsds')
#poly = shape(feature['geometry'])
#poly = MultiPolygon(coors, context_type='geojson')
# check each polygon to see if it contains the point
for feature in js['features']:
    if feature['geometry'] != None:
        polygon = shape(feature['geometry'])
#     coors = feature['geometry']['coordinates']
#     print(len(coors))
#     poly = MultiPolygon(coors)
        if polygon.contains(point):
            print('Found containing polygon:', feature['properties'])