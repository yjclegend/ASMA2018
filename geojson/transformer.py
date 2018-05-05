import json
src = open('SA3_GEO.json')
src_json = json.load(src)

features = src_json['features']
print(len(features))
# new_features = list()
# for feature in features:
# 	properties = feature['properties']
# 	if properties['GCC_CODE16'] == '2GMEL':
# 		new_features.append(feature)
# src_json['features'] = new_features
# tar = open('SA2_GEO.json', 'w')
# tar.write(json.dumps(src_json,indent=2))