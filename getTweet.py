# -*- coding: utf-8-*-
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
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
            with open('python.json', 'a') as f:
                print(status.text)
                f.write(status.text)
                f.flush()
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True

# australia = api.geo_search(query="australia", granularity="country")
# place_id = australia[0].id
# melbourne = api.geo_search(query="melbourne", granularity="city")
# #print(melbourne[0])
# center = melbourne[0].centroid
# print(center)
geo_code = str(145) + ',' + str(-37.5) + ',' + '2km'
print(geo_code)
tweets = api.search(geocode="38.376,-0.5,8km",lang='en',rpp=100)
for tweet in tweets:
    print(tweet.text)