import json
import pandas as pd
import matplotlib.pyplot as plt

def getdata():
    tweets_data_file = "../Data/tweets_data.txt"

    tweets_data = []
    try:
        with open(tweets_data_file,'r') as json_obj:
            tweets_data = json.loads(json_obj.read())
    except Exception as e:
        print("Error",e)
    
    tweets = pd.DataFrame()

    # storing lang data to data frame tweets
    tweets['lang'] = [tweet.get('lang','') for tweet in tweets_data]

    #counting all languages
    tweets_by_lang = tweets['lang'].value_counts()

    # storing country data to data frame tweets
    #tweets['country'] = [tweet['place'].get('country','') for tweet in tweets_data]
    #tweets_by_country= tweets['country'].value_counts()

    getTopLanguagesOfTweets(tweets_by_lang)
    #getTopCountryOfTweets()

    tweets_hashtags = []
    hashtags_data = [tweet['entities'].get('hashtags','') for tweet in tweets_data]

    for hashtag in hashtags_data:
        if(len(hashtag)!=0):
            for i in range(len(hashtag)):
                tweets_hashtags.append(hashtag[i]['text'])

    tweets['hashtags'] = pd.Series(tweets_hashtags)
    tweets_by_hashtags = tweets['hashtags'].value_counts()
    getTopHashtagsOfTweets(tweets_hashtags)
    #tweets_by_hashtags = tweets_hashtags.count()

def getTopLanguagesOfTweets(languages_data):
    fig, ax = plt.subplots()
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_xlabel('Languages', fontsize=15)
    ax.set_ylabel('Number of tweets' , fontsize=15)
    ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
    languages_data.plot(ax=ax, kind='bar', color='red')
    
# def getTopCountryOfTweets():
#     fig, ax = plt.subplots()
#     ax.tick_params(axis='x', labelsize=15)
#     ax.tick_params(axis='y', labelsize=10)
#     ax.set_xlabel('Country', fontsize=15)
#     ax.set_ylabel('Number of tweets' , fontsize=15)
#     ax.set_title('Top Country', fontsize=15, fontweight='bold')
#     tweets_by_country.plot(ax=ax, kind='bar', color='red')

def getTopHashtagsOfTweets(hashtag_data):
    fig, ax = plt.subplots()
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_xlabel('Hashtags', fontsize=15)
    ax.set_ylabel('Number of tweets' , fontsize=15)
    ax.set_title('Top Used Hashtags', fontsize=15, fontweight='bold')
    hashtag_data[:10].plot(ax=ax, kind='bar', color='red')    