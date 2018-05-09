# -*- coding: utf-8-*-
#This document is used to load json files which contain the original data of the tweets, 
#divide these tweets into corresponding suburbs, 
#make sentiment analysis of the content that each tweet published on Twitter, 
#count the number of tweet based on different kinds of keywords and 
#get the total number of the tweets in each suburb.
#As a result, it will produce a json file named 'conclusions' that includes all dealt data we need.

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
        conclusion = {'pos_count': posCount,'neg_count': negCount,'pos_rate': posPercent}
        return conclusion
    
    #count the number of tweet based on different kinds of keywords and \
    #get the total number of the tweets in each suburb.
    def countTweets(self,data, keywords):
        #print("keywords", keywords)
        tweetinKeywords={'sports': 0, 'entertainments': 0, 'food&drink': 0}
        tweetinArea=0
        for temp in data:
            text=temp['value']['text']
            for kind in keywords:
                for word in keywords[kind]:
                    if word in text.lower():
                        tweetinKeywords[kind] +=1
            tweetinArea +=1
        result ={'tweets_belong_sports_Percent': tweetinKeywords['sports']/tweetinArea,'tweets_belong_entertainments_Percent': \
                 tweetinKeywords['entertainments']/tweetinArea, 'tweets_belong_food&drinks_Percent': tweetinKeywords['food&drink']/tweetinArea,\
                'tweets_in_Area': tweetinArea}
        return result
            
        
    #input: text json 
    #output: text json has key words count; support rate
    def filterKeyword(self, data, keywords):
        if len(keywords) == 0:
            return data
        filtered = list()
        for t in data:
            for keyword in keywords:
                if keyword in t['value']['text'].lower():
                    filtered.append(t)
                    print(t['value']['text'].encode('utf-8'))
        return filtered

    def partitionByCoor(self, data):
        part = dict()
        self.loadGeo('geojson/SA3_GEO.json')
        self.buildPolygons('SA3_CODE16')
        for t in data:
            coor = t['value']['coordinates']
            point = Point(coor[0], coor[1])
            code = self.pointInPoly(point)
            if code not in part:
                part[code] = list()
            part[code].append(t)
        return part

    def buildPolygons(self, level):
        features = self.geojson['features']
        self.polygons = dict()
        for feature in features:
            if feature['geometry'] != None:
                code = feature['properties'][level]
                self.polygons[code] = shape(feature['geometry'])

    def pointInPoly(self, point):
        for code in self.polygons:
            if self.polygons[code].contains(point):
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
        part = self.partitionByCoor(data)
        conclusions = dict()
        for code in part:
            senti = self.sentiment(part[code])
            tweetinKeywords = self.countTweets(part[code], keywords)
            combine=dict(senti, **tweetinKeywords)
            conclusions[code] = combine
        tar = open('conclusions.json','w')
        tar.write(json.dumps(conclusions, indent=2))
                

if __name__ == '__main__':
    ta = TweetAnalyze()
    keywords = dict()
    keywords={'sports':{'sports','cycling','swimming','tennis','soccer','riding','footy','football','jogging','running','hiking','frisbee',\
              'yoga','marathon','gymnastics','basketball','boxing','badminton','skiing','fitness'},'entertainments':\
             {'entertainments','wedding','shopping','party','birthday','music','movie','the avenger','peter rabbit',\
              'lsle of dogs'},'food&drink':{'barbecue','bbq','food','cake','bread','milk','cocktail','coke','alcohol','beer','wine','juice'}}
    ta.scenario2(keywords)
    
    
