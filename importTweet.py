
# -*- coding: utf-8-*-
from urllib import request
import json
import csv

class TwImport(object):
    """docstring for TwImport"""
    def __init__(self, ):
        super(TwImport, self).__init__()
        self.db_url = 'http://115.146.84.11:5984/twitter/_bulk_docs'
        self.user = 'admin'
        self.password = 'admin'     

    def importFromCsv(self):
        tweets = dict()
        tweets["docs"] = list()
        with open('geoTweets-Melb.csv', newline='', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            count = 0
            for row in spamreader:
                try:
                    text = row[10]
                    create = row[2]
                    lati = float(row[8])
                    longi = float(row[9])
                    data = {'text': text, 'coordinates': [longi,lati], 'time': create}
                    tweets["docs"].append(data)
                    count += 1
                    #self.addDocument(data)
                except Exception as e:
                    print(e)
            print(count)
            params = json.dumps(tweets, default=str)#.encode('utf-8')
            datafile = open('tweetdata.json', 'w', encoding='utf-8')
            datafile.write(params)
        
        #self.addDocument(tweets)
                
    def addDocument(self, data):
        params = json.dumps(data, default=str).encode('utf-8')
        password_mgr = request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, self.db_url, self.user, self.password)
        handler = request.HTTPBasicAuthHandler(password_mgr)
        opener = request.build_opener(handler)
        request.install_opener(opener)
        req =  request.Request(self.db_url, data=params, headers={'Content-Type': 'application/json'}) 
        resp = request.urlopen(req)
        print(resp.read())

if __name__ == '__main__':
    ti = TwImport()
    ti.importFromCsv()