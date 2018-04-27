# -*- coding: utf-8-*-
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from urllib import request, parse
import json
import time

class MyListener(StreamListener):
    def __init__(self, ):
        super(MyListener, self).__init__()
        self.db_url = 'http://115.146.86.21:5984/yjc'
        self.user = 'admin'
        self.password = 'admin'
    
    def on_status(self, status):
        try:
            with open('text_coor.json', 'a') as f:
                coor = status.coordinates
                print('coor = ', coor)
                if coor != None:
                    text = status.text
                    data = {'text': text, 'coordinates': coor.get('coordinates')}
                    self.addDocument(data)
                    f.write(json.dumps(data) + '\n')
                    f.flush()
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print('on_error = ', status)
        return True

    def addDocument(self, data):
        params = json.dumps(data).encode('utf-8')
        password_mgr = request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, self.db_url, self.user, self.password)
        handler = request.HTTPBasicAuthHandler(password_mgr)
        opener = request.build_opener(handler)
        request.install_opener(opener)
        req =  request.Request(self.db_url, data=params, headers={'content-type': 'application/json'}) 
        resp = request.urlopen(req)
        print(resp.read())

class TweetHarvester(object):
    """docstring for TweetHarvester"""
    def __init__(self, ):
        super(TweetHarvester, self).__init__()
        self.consumer_key = '1az5VnYmc4oy0faljLdSxvrzC'
        self.consumer_secret = 'NrEluXS9IGzGVru23sajuVClBXW6dbtx4MMNNO7LnLbD2otgAm'
        self.access_token = '833522486792777728-D99ckOM06s4VR4DG34YrODB2n9GQMs2'
        self.access_secret = 'UvDk8grNKrDkCl37hTJbVABCPwo3yGxr3b1o8KNLzqAuz'

        
        self.initAPI()

    def initAPI(self):
        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_secret)
        self.api = tweepy.API(self.auth)
    
    def startListener(self):
        twitter_stream = Stream(self.auth, MyListener())
        twitter_stream.filter(locations=[112.921114,-43.740482,159.109219,-9.142176])

if __name__ == '__main__':
    th = TweetHarvester()
    th.startListener()
