from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json

#Variables that contains the user credentials to access Twitter API 
consumer_key = 'd0ij9YCPLuVY4lx8A1p33Qj7A'
consumer_secret = 'gvV3WVgIie66YwXWCD6nPDASDSMDWXpBMgN2AeHSyfLeU3tt1B'
access_token = '911800711897219072-ELzUb8qGSDcZj5gE4SdZVU9a7rgqIWl'
access_token_secret = 'euJh28JOlyQedATx2fUG9EC8sJKxPJoW3dJ2T64cjdTVP'

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def __init__(self,num_of_tweets,tweets_data_file):
        
        #counter to fetch num_of_tweets data
        self.counter=0
        self.num_of_tweets = num_of_tweets
        
        #data file
        self.tweets_data_file = tweets_data_file
        
    def on_data(self, data):
        
        if(self.counter < self.num_of_tweets):
            #reading tweet
            tweet_data = json.loads(data)
            self.counter = self.counter + 1
            print(self.counter)
            try: 
                #print(tweet_data)
                #print("--------------------------------------------------------")
                self.tweets_data_file.write(json.dumps(tweet_data))
                self.tweets_data_file.write(",")
            except Exception as e:
                print(e)
            
            return True
        else:
            return False

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    num_of_tweets=100
    tweets_data_file = open('../Data/tweets_data.txt', 'w', encoding='utf-8')
    tweets_data_file.write("[")
    listner = StdOutListener(num_of_tweets,tweets_data_file)
    
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    #keyword = "#whitehouse"
    twitter_stream = Stream(auth, listner)
    twitter_stream.filter(track=['#NBAAllStarGame'])    

    tweets_data_file.write("]")