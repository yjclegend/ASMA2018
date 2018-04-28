#  COMP90024 Cloud & Cluster Computing
#  Assignment 2
#  This file is to grab tweets from Twitter


# -*- coding: utf-8-*-
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from urllib import request
import json
import twitterKey as tKey

class MyListener(StreamListener):
    def __init__(self, ):
        super(MyListener, self).__init__()
        self.db_url = 'http://115.146.86.21:5984/yjc'
        self.user = 'admin'
        self.password = 'admin'
        self.process_num = 4
        self.process_id = tKey.process_id
    
    def on_status(self, status):
        try:
            # coor = status.coordinates  # Coordinate of the tweet
            # if coor != None:
            #     tweetTime = status.created_at  # Posting time of the tweet
            #     second = tweetTime.second  # Seconds of the posting time
            #     text = status.text  # Text of the tweet
            #     data = {'text': text, 'coordinates': coor.get('coordinates'), 'time': tweetTime}
            #
            #     if second % self.process_num == self.process_id:
            #         self.addDocument(data)
            # return True

            # --------------Test: write in file---------------------

            coor = status.coordinates
            if coor != None:
                text = status.text
                tweetTime = status.created_at
                data = {'text': text, 'coordinates': coor.get('coordinates'), 'time': tweetTime}
                second = tweetTime.second
                fileID = second % self.process_num
                docName = 'text_coor' + str(fileID) + '.json'
                with open(docName, 'a') as f:
                    # f.write(str(fileID) + '@@@' + json.dumps(data) + '\n')
                    f.write(json.dumps(data, default=str).encode('utf-8') + '\n')
                    f.flush()
                print('second = ', second)
                print('fileID = ', fileID)
            return True

        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print('on_error = ', status)
        return True

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

class TweetHarvester(object):
    """docstring for TweetHarvester"""
    def __init__(self, ):
        super(TweetHarvester, self).__init__()
        self.consumer_key = tKey.consumer_key
        self.consumer_secret = tKey.consumer_secret
        self.access_token = tKey.access_token
        self.access_secret = tKey.access_secret

        
        self.initAPI()

    def initAPI(self):
        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_secret)
        self.api = tweepy.API(self.auth)
    
    def startListener(self):
        twitter_stream = Stream(self.auth, MyListener())
        while True:
            try:
                twitter_stream.filter(locations=[112.921114,-43.740482,159.109219,-9.142176])
            except Exception as e:
                print(e)

if __name__ == '__main__':
    th = TweetHarvester()
    th.startListener()
