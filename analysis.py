#This document is to get data from specific location,
#do sentiment analysis and count the number of positive/nagative tweets
import json
from textblob import TextBlob
from urllib import request
 

# input: specific location data
# output: print('positive count:',self.posCount, 'negative count:',self.nagCount)
class Analysis():

    def __init__(self, location):
        self.url = 'http://115.146.85.216:5984/twitter/_design/coor/_view/tweet_in_'
        self.url = self.url + location
        self.username = 'admin'
        self.password = 'admin'
        
        self.posCount = 0
        self.nagCount = 0
        
    # sentiment analysis and count positive/nagative
    # from text json list 
    def count(self,textRows):
        for t in textRows:
            # json to string
            twitter = json.dumps(t)
            tText = TextBlob(twitter)
            result = tText.sentiment
            if result.polarity >= 0.1:
                self.posCount = self.posCount + 1
            else :
                if result.polarity <= 0.1:
                    self.nagCount = self.nagCount + 1
        
        posPercent = self.posCount/(self.posCount+self.nagCount)
        countDic = {'positive count:': self.posCount,'negative count:': self.nagCount,'positive rate': posPercent}
        countJson = json.dumps(countDic)
        print('positive count:',self.posCount, 'negative count:',self.nagCount,'positive rate:', posPercent)
        return countJson
    #get data from specific location
    def getData(self):
        password_mgr = request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, self.url, self.username, self.password)
        handler = request.HTTPBasicAuthHandler(password_mgr)
        opener = request.build_opener(handler)
        request.install_opener(opener)
        req =  request.Request(self.url) 
        data = request.urlopen(req).read()
        return data

    #return twitter text as json object list
    def processData(self,data):
        wholeJsonObject = json.loads(data)
        dataRows = wholeJsonObject['rows']
        textRows = []
        for line in dataRows:
            textRows.append(line['value']['text'])
        return textRows       


    #input: text json 
    #output: text json has key words count; support rate
    def getKeywordText(self,textRows,keywords):
        keywordTexts = []
        kPosCount = 0
        kNagCount = 0
        for text in textRows:
            for keyword in keywords:
                if keyword in text:
                    print(text)
                    keywordTexts.append(text)
        for keywordText in keywordTexts:
            kText = TextBlob(keywordText)
            kresult = kText.sentiment
            if kresult.polarity >= 0.1:
                kPosCount = kPosCount + 1
            else :
                if kresult.polarity <= 0.1:
                    kNagCount = kNagCount + 1
        
        supportRate = kPosCount/(kPosCount+kNagCount)
        
        print('Text has key word:',(kPosCount+kNagCount), 'support rate:',supportRate)
        
        

if __name__ == '__main__':
    analysis = Analysis("perth")
    analysis.count(analysis.processData(analysis.getData()))
    
    analysis.getKeywordText(analysis.processData(analysis.getData()),['weather','sun','sea'])




        
