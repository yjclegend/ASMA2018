# -*- coding: utf-8-*-
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import urllib.request as request
import json
import time

# Keys and authorization of Twitter.
consumer_key = '1az5VnYmc4oy0faljLdSxvrzC'
consumer_secret = 'NrEluXS9IGzGVru23sajuVClBXW6dbtx4MMNNO7LnLbD2otgAm'
access_token = '833522486792777728-D99ckOM06s4VR4DG34YrODB2n9GQMs2'
access_secret = 'UvDk8grNKrDkCl37hTJbVABCPwo3yGxr3b1o8KNLzqAuz'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

url = 'admin:admin@115.146.86.21/yjc'

# Tweepy listener method.
class MyListener(StreamListener):
    def on_status(self, status):
        coor = status.coordinates
        print('coor = ', coor)
        if coor != None:
            text = status.text
            values = {'text': text, 'coordinates': coor.get('coordinates')}
            data = json.dumps(values)
            header_key = 'Content-Type'
            header_val = 'application/json'
            response = request.Request(url, data)
            response.add_header(header_key, header_val)
            print('response = ', response)
        return True

coordinates = [[112.921114, -43.740482],
               [112.921114, -9.142176],
               [159.109219, -9.142176],
               [159.109219, -43.740482],
               [112.921114, -43.740482]]

# Filter tweets and only get those in Australia
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(locations=[112.921114, -43.740482, 159.109219, -9.142176])

# db=MySQLdb.connect(host='localhost', user='XXX', passwd='XXX', db='twitter')
# db.set_character_set('utf8')

# curl -X POST -H "Content-Type: application/json" admin:admin@115.146.86.21/yjc -d '{"key":"value"}'
