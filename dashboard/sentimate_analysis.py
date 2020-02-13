from django.shortcuts import render
from django.http import HttpResponse

import re 
import tweepy 
import matplotlib.pyplot as plt
from tweepy import OAuthHandler 
from textblob import TextBlob 

class TwitterClient(object): 
	''' 
	Generic Twitter Class for sentiment analysis. 
	'''
	def __init__(self): 
		''' 
		Class constructor or initialization method. 
		'''
		# keys and tokens from the Twitter Dev Console 
		consumer_key = 'd0ij9YCPLuVY4lx8A1p33Qj7A'
		consumer_secret = 'gvV3WVgIie66YwXWCD6nPDASDSMDWXpBMgN2AeHSyfLeU3tt1B'
		access_token = '911800711897219072-ELzUb8qGSDcZj5gE4SdZVU9a7rgqIWl'
		access_token_secret = 'euJh28JOlyQedATx2fUG9EC8sJKxPJoW3dJ2T64cjdTVP'

		# attempt authentication 
		try: 
			# create OAuthHandler object 
			self.auth = OAuthHandler(consumer_key, consumer_secret) 
			# set access token and secret 
			self.auth.set_access_token(access_token, access_token_secret) 
			# create tweepy API object to fetch tweets 
			self.api = tweepy.API(self.auth) 
		except: 
			print("Error: Authentication Failed") 

	def clean_tweet(self, tweet): 
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

	def get_tweet_sentiment(self, tweet): 
		''' 
		Utility function to classify sentiment of passed tweet 
		using textblob's sentiment method 
		'''
		# create TextBlob object of passed tweet text 
		analysis = TextBlob(self.clean_tweet(tweet)) 
		# set sentiment 
		if analysis.sentiment.polarity > 0: 
			return 'positive'
		elif analysis.sentiment.polarity == 0: 
			return 'neutral'
		else: 
			return 'negative'

	def get_tweets(self, query, count ): 
		''' 
		Main function to fetch tweets and parse them. 
		'''
		# empty list to store parsed tweets 
		tweets = [] 

		try: 
			# call twitter api to fetch tweets 
			fetched_tweets = self.api.search(q = query, count = count) 

			# parsing tweets one by one 
			for tweet in fetched_tweets: 
				# empty dictionary to store required params of a tweet 
				parsed_tweet = {} 

				# saving text of tweet 
				parsed_tweet['text'] = tweet.text 
				# saving sentiment of tweet 
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

				# appending parsed tweet to tweets list 
				if tweet.retweet_count > 0: 
					# if tweet has retweets, ensure that it is appended only once 
					if parsed_tweet not in tweets: 
						tweets.append(parsed_tweet) 
				else: 
					tweets.append(parsed_tweet) 

			# return parsed tweets 
			return tweets 

		except tweepy.TweepError as e: 
			# print error (if any) 
			print("Error : " + str(e)) 

def main(request): 
    # creating object of TwitterClient Class 
    api = TwitterClient()
    # calling function to get tweets 
    keyword = request.GET['keyword']
    tweets = api.get_tweets(query = keyword, count = 100000) 

    print("------------------------------------------------------------------------------------------------")
    print(tweets)
    print("------------------------------------------------------------------------------------------------")

    # picking positive tweets from tweets 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 

	#storing result in list...

    # percentage of positive tweets 
    sa_result_pv = round( (100*len(ptweets)/len(tweets)), 2)

    # picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    
	# percentage of neutral tweets 
    sa_result_nt = round( (100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)) , 2 )
	
	# percentage of negative tweets 
    sa_result_nv = round( (100*len(ntweets)/len(tweets)) , 2)

    
    # printing first 5 positive tweets 
    print("\n\nPositive tweets:") 
    for tweet in ptweets: 
        print(tweet['text']) 

    # printing first 5 negative tweets 
    print("\n\nNegative tweets:") 
    for tweet in ntweets: 
        print(tweet['text'])
    
    return render(request,'dashboard.html',{'pv':sa_result_pv,'nt':sa_result_nt,'nv':sa_result_nv,'keyword':keyword})