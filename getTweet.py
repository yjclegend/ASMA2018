import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
 
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
 
myStreamListener = MyListener()
myStream = tweepy.Stream(auth = api.auth, listener=MyListener())
myStream.filter(track=['china'])