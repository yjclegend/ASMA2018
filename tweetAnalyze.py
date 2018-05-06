# -*- coding: utf-8-*-
from urllib import request
import json
from textblob import TextBlob
from shapely.geometry import shape, Point

class TweetAnalyze(object):
    """docstring for TweetAnalyze"""
    def __init__(self, ):
        super(TweetAnalyze, self).__init__()
        self.db_url = "http://115.146.85.216:5984/twitter"
        self.view_url = 'http://115.146.85.216:5984/twitter/_design/coor/_view/'
        self.user = 'admin'
        self.password = 'admin'
        self.cities = ['melbourne', 'brisbane','sydney', 'adelaide','canberra','darwin','hobart','perth']
        self.installOpener()
        #self.loadGeo()

    def loadGeo(self, geo):
        geofile = open(geo)
        self.geojson = json.load(geofile)

    def installOpener(self):
        password_mgr = request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, self.db_url, self.user, self.password)
        handler = request.HTTPBasicAuthHandler(password_mgr)
        opener = request.build_opener(handler)
        request.install_opener(opener)
    

    # retrive data from db,
    # returns a list of tweet with full info
    def getData(self, url):
        print(url)
        req =  request.Request(url) 
        resp = request.urlopen(req).read()
        return self.getRows(resp)

    def getDataInCity(self, city):
        return self.getData(self.view_url + 'tweet_in_' + city)

    def getRows(self,data):
        wholeJsonObject = json.loads(data)
        dataRows = wholeJsonObject['rows']
        return dataRows

    def sentiment(self,data):
        posCount = 0
        negCount = 0
        for t in data:
            # json to string
            twitter = t['value']['text']
            #print(twitter.encode('utf-8').decode('gbk'))
            #exit()
            tText = TextBlob(twitter)
            result = tText.sentiment
            if result.polarity > 0.0:
                posCount += 1
            if result.polarity < 0.0 :
                negCount += 1
        
        posPercent = posCount / (posCount + negCount)
        conclusion = {'pos_count:': posCount,'neg_count:': negCount,'pos_rate': posPercent}
        return conclusion


    #input: text json 
    #output: text json has key words count; support rate
    def filterKeyword(self, data, keywords):
        filtered = list()
        for t in data:
            for keyword in keywords:
                if keyword in t['value']['text'].lower():
                    filtered.append(t)
                    print(t['value']['text'].encode('utf-8'))
        return filtered

    def partitionByCoor(self, data):
        part = dict()
        locations = list()
        self.loadGeo('genjson/SA3_GEO.json')
        self.buildPolygons('SA3_CODE16')
        for t in data:
            coor = t['value']['coordinates']
            locations.append({'lng': coor[0],'lat': coor[1]})
            point = Point(coor[0], coor[1])
            code = self.pointInPoly(point)
            if code not in part:
                part[code] = list()
            part[code].append(t)
        return part, locations

    def buildPolygons(self, level):
        features = self.geojson['features']
        self.polygons = dict()
        for feature in features:
            if feature['geometry'] != None:
                code = feature['properties'][level]
                self.polygons[code] = shape(feature['geometry'])

    def pointInPoly(self, point):
        for code, polygon in self.polygons:
            if polygons.contains(point):
                return code

    
    def spectrum(self, src, key):
        features = src['features']
        minVal = -1
        maxVal = 0
        for feature in features:
            properties = feature['properties']
            if int(properties[key]) < minVal or minVal == -1:
                minVal = properties[key]
            if int(properties[key]) > maxVal:
                maxVal = properties[key]
        return (minVal, maxVal)

    def getColor(self, code, color_src, spectrum, region_key, data_key):
        minVal, maxVal = spectrum
        features = color_src['features']
        for feature in features:
            properties = feature['properties']
            gcc_code = properties[region_key]
            if gcc_code == code:
                value = properties[data_key]
                color = int(255 - 255 * (value - minVal) / (maxVal - minVal))
                color_str = str(hex(color))[2:]
                if color < 16:
                    color_str = '0' + color_str
                return '#ff' + color_str + color_str

    def geoProperty(self, geofile, data_file, region_key, data_key):
        color_file = open(data_file)
        color_src = json.load(color_file)
        spectrum = self.spectrum(color_src, data_key)
        geo_file = open(geofile)
        geo_json = json.load(geo_file)
        features = geo_json['features']
        for feature in features:
            properties = feature['properties']
            code = properties['GCC_CODE16']
            properties['color'] = self.getColor(code, color_src, spectrum, region_key, data_key)
        tar_file = open('geojson/tar.json','w')
        tar_file.write(json.dumps(geo_json,indent=2))

    def scenario1(self):
        conclusions = dict()
        for city in self.cities:
            data = self.getDataInCity(city)
            senti = self.sentiment(data)
            conclusions[city] = senti
        return conclusions

    def scenario2(self, keywords):
        data = self.getDataInCity('melbourne_coor')
        print(len(data))
        filtered = self.filterKeyword(data, keywords)
        print(len(filtered))
        # part, locations = self.partionsByCoor(filtered)
        # conclusions = dict()
        # for code, datalist in part:
        #     senti = self.sentiment(datalist)
        #     conclusions[code] = senti
        # return conclusions

if __name__ == '__main__':
    ta = TweetAnalyze()
    keywords = ["marvel","avengers","infinity war","infinity stone","iron man","tony stark","robert downey jr.","captain","steve rogers","chris evans","winter soldier","hulk","bruce banner","edward norton","thor","loki","tom hiddleston","ant-man","paul rudd","doctor strange","guardians of the galaxy","chris pratt","dark aste","groot","spider-man","peter parker","ultron","black panther","wakanda","deadpool","wade wilson"]
    keywords = ["gay","marriage equality","equalmarriage","letusmarry","rainbowdirection","same-sex couple","same-sex marriage","lgbt","queer","lesbian","straight","bisexual","transgender"]
    keywords = ['trump']
    ta.scenario2(keywords)
    #data = ta.getDataInCity('melbourne')
    
    #ta.sentiment(data)

    #ta.geoProperty('geojson/GCC_GEO.json' ,'geojson/GCC_POPULATION.json', 'gcc_code16', 'erp_p_tot_cnt')
    
