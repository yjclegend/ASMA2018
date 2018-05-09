# -*- coding: utf-8-*-
#This document is used to fetch AURIN data with the username and password through url.

from urllib import request
import json

class GeoAurin(object):
    """docstring for GeoAurin"""
    def __init__(self, ):
        super(GeoAurin, self).__init__()
        self.base_url = 'http://openapi.aurin.org.au/wfs?outputFormat=application/json&request=GetFeature&version=1.0.0&TYPENAME='
        self.username = 'student'
        self.password = 'dj78dfGF'

    def fetchData(self, dataset):
        url = self.base_url + dataset
        password_mgr = request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, url, self.username, self.password)
        handler = request.HTTPBasicAuthHandler(password_mgr)
        opener = request.build_opener(handler)
        request.install_opener(opener)
        req =  request.Request(url) 
        resp = request.urlopen(req)
        out = open('out.json', 'w')
        out.write(resp.read().decode('utf-8'))


if __name__ == '__main__':
    ga = GeoAurin()
    dataset = 'aurin:datasource-au_govt_dss-UoM_AURIN_national_public_toilets_2017'
    ga.fetchData(dataset)
