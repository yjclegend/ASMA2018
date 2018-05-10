# -*- coding: utf-8-*-
"""
Author:
    Team2
Members:
    Jiachuan Yu(867000), jiachuany
    Mengyu Zhou(780956), mengyuz2
    Chenxi Hou(811596), chou1
    Surong Zhu(859160), surongz
    Sicong Ma(884092), Sicongm

"""

from urllib import request
import sys
import json
import shapefile

class GeoImport(object):
    """docstring for GeoImport"""
    def __init__(self, ):
        super(GeoImport, self).__init__()
        self.shape_src = sys.argv[1]
        self.db_url = 'http://115.146.84.11:5984/geo/_bulk_docs'
        self.user = 'admin'
        self.password = 'admin'
        self.geos = dict()
        self.geos['docs'] = list()

    #convert shapefile to geo json
    def shptojson(self):
        reader = shapefile.Reader(self.shape_src)
        fields = reader.fields[1:]
        field_names = [field[0] for field in fields]
        count = 0
        for sr in reader.shapeRecords():
            count += 1
            atr = dict(zip(field_names, sr.record))
            geom = sr.shape.__geo_interface__
            feature = dict(type="Feature", geometry=geom, properties=atr)
            self.geos['docs'].append(feature)
            if count >= 100:
                self.addDocument(self.geos)
                count = 0
                self.geos['docs'] = list()
        self.addDocument(self.geos)


    def addDocument(self, data):
        params = json.dumps(data, default=str).encode('utf-8')
        password_mgr = request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, self.db_url, self.user, self.password)
        handler = request.HTTPBasicAuthHandler(password_mgr)
        opener = request.build_opener(handler)
        request.install_opener(opener)
        req =  request.Request(self.db_url, data=params, headers={'content-type': 'application/json'}) 
        resp = request.urlopen(req)
        print(resp.read())


if __name__ == '__main__':
    shape_src = sys.argv[1]
    gi = GeoImport()
    gi.shptojson()