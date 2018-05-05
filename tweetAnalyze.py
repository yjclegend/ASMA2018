# -*- coding: utf-8-*-
from urllib import request
import json
from textblob import TextBlob

class TweetAnalyze(object):
    """docstring for TweetAnalyze"""
    def __init__(self, ):
        super(TweetAnalyze, self).__init__()
        self.db_url = "http://115.146.85.216:5984/twitter"
        self.view_url = 'http://115.146.85.216:5984/twitter/_design/coor/_view/'
        self.user = 'admin'
        self.password = 'admin'
        self.installOpener()

    def installOpener(self):
        password_mgr = request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, self.db_url, self.user, self.password)
        handler = request.HTTPBasicAuthHandler(password_mgr)
        opener = request.build_opener(handler)
        request.install_opener(opener)
    
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
        countDic = {'pos_count:': posCount,'neg_count:': negCount,'pos_rate': posPercent}
        countJson = json.dumps(countDic)
        

if __name__ == '__main__':
    ta = TweetAnalyze()
    data = ta.getDataInCity('perth')
    ta.sentiment(data)
    
