import json
src = open('SA3_GEO_INCOME.json')
src_json = json.load(src)

data_src = open('SA3_INCOME.json')
data_json = json.load(data_src)



geo_features = src_json['features']
data_features = data_json['features']

for feature in geo_features:
	properties = feature['properties']
	code = properties['SA3_CODE16']
	for inc in data_features:
		inc_prop = inc['properties']
		if inc_prop['sa3_code16'] == code:
			properties['per_inc_weekly'] = inc_prop['median_tot_prsnl_inc_weekly']
			break

	
tar = open('SA3_GEO_INCOME.json', 'w')
tar.write(json.dumps(src_json, indent=2))