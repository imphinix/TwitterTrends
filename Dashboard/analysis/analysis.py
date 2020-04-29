import json
import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = 'C:\\Users\\BURPY\\Desktop\\TwitterTrends\\'
path = BASE_DIR + 'Data/tweets_data.txt'

tweets_data = []
try:
    with open(path,'r') as json_obj:
        tweets_data = json.loads(json_obj.read())
except Exception as e:
    print("Error",e)
    
tweets = pd.DataFrame()

def getHashtagData():
    hashtags_list = []
    hashtags_data = [tweet['entities'].get('hashtags','') for tweet in tweets_data]

    for hashtag in hashtags_data:
        if(len(hashtag)!=0):
            for i in range(len(hashtag)):
                hashtags_list.append(hashtag[i]['text'])

    nHashtag_list = [] 
    hashtag_count_list = []

    for hashtag in hashtags_list:
        if hashtag not in nHashtag_list:
            nHashtag_list.append(hashtag)
        
    for hashtag in nHashtag_list:
        hashtag_count_list.append(hashtags_list.count(hashtag))

    return nHashtag_list , hashtag_count_list


def getLanguageData():

    tweets['lang'] = [tweet.get('lang','') for tweet in tweets_data]
    
    language_list = [] 
    nLanguage_list = [] 
    language_count_list = []
        
    for language in tweets['lang']:
        language_list.append(language)

    for language in tweets['lang']:
        if language not in nLanguage_list:
            nLanguage_list.append(language)
        
    for language in nLanguage_list:
        language_count_list.append(language_list.count(language))

    return nLanguage_list , language_count_list

def getRtOrgRatio():
    tweets['text'] = [tweet.get('text','') for tweet in tweets_data]

    retweet_count = 0
    original_count = 0

    for text in tweets['text']:
        if 'RT' in text:
            retweet_count = retweet_count + 1
        else:
            original_count = original_count + 1

    return ( retweet_count , original_count )

def getCountData():
    rtorgCount = getRtOrgRatio()
    
    total_post = 100
    total_user = total_post - rtorgCount[0]
    total_reach = 0
    users_data = [tweet.get('user','') for tweet in tweets_data]

    for user in users_data:
        total_reach = total_reach + int(user.get('followers_count','')) + int(user.get('friends_count','')) 

    return (total_post, total_user , total_reach)