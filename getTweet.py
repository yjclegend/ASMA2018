# -*- coding: utf-8-*-
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import urllib
import json
import time
 
consumer_key = '1az5VnYmc4oy0faljLdSxvrzC'
consumer_secret = 'NrEluXS9IGzGVru23sajuVClBXW6dbtx4MMNNO7LnLbD2otgAm'
access_token = '833522486792777728-D99ckOM06s4VR4DG34YrODB2n9GQMs2'
access_secret = 'UvDk8grNKrDkCl37hTJbVABCPwo3yGxr3b1o8KNLzqAuz'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)


# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)
class MyListener(StreamListener):
    def on_status(self, status):
        try:
            with open('text_coor.json', 'a') as f:
                coor = status.coordinates
                print('coor = ', coor)
                if coor != None:
                    text = status.text
                    data = {'text': text, 'coordinates': coor.get('coordinates')}
                    # print('type = ', type(json.dumps(data)))
                    f.write(json.dumps(data) + '\n')
                    f.flush()
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print('on_error = ', status)
        return True

# australia = api.geo_search(query="australia", granularity="country")
# # place_id = australia[0].id
# #melbourne = api.geo_search(query="melbourne", granularity="city")
# Box = australia[0].bounding_box
# print(Box.coordinates)
coordinates =  [[112.921114, -43.740482], 
                [112.921114, -9.142176], 
                [159.109219, -9.142176], 
                [159.109219, -43.740482], 
                [112.921114, -43.740482]]
# center = melbourne[0].centroid
# print(center)
# geo_code = str(38.376) + ',' + str(-0.5) + ',' + '20km'
# print(geo_code)
# while True:
#     try:
#         tweets = api.search(geocode=geo_code,lang='en',rpp=100)
#         for tweet in tweets:
#             print(tweet.text)
#     except Exception as e:
#         print(e)

twitter_stream = Stream(auth, MyListener())

twitter_stream.filter(locations=[112.921114,-43.740482,159.109219,-9.142176])

# db=MySQLdb.connect(host='localhost', user='XXX', passwd='XXX', db='twitter')
# db.set_character_set('utf8')

# curl -X POST -H "Content-Type: application/json" admin:admin@127.0.0.1:5984/yjc -d '{"key":"value"}'

header = {}