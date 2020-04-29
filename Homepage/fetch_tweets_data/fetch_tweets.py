import tweepy
import json
import os
from django.shortcuts import render ,redirect

def getdata(request):

    consumer_key = 'd0ij9YCPLuVY4lx8A1p33Qj7A'
    consumer_secret = 'gvV3WVgIie66YwXWCD6nPDASDSMDWXpBMgN2AeHSyfLeU3tt1B'
    access_token = '911800711897219072-ELzUb8qGSDcZj5gE4SdZVU9a7rgqIWl'
    access_token_secret = 'euJh28JOlyQedATx2fUG9EC8sJKxPJoW3dJ2T64cjdTVP'


    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    print("connection done....")

    query = request.GET['keyword']

    #tweets_data_file = open('../Data/tweets_data.txt', 'w', encoding='utf-8')
    #path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'Data/tweets_data.txt')
    
    BASE_DIR = 'C:\\Users\\BURPY\\Desktop\\TwitterTrends\\'
    path = BASE_DIR + 'Data/tweets_data.txt'
    
    tweets_data_file = open(path, 'w', encoding='utf-8')

    tweets_data_file.write("[")
    
    tweets=tweepy.Cursor(api.search,q=query).items(100)

    i=0
    for tw in tweets:
        print(i)
        i=i+1
        status = tw
        json_str = json.dumps(status._json)
        tweets_data_file.write(json_str)
        tweets_data_file.write(",")

    tweets_data_file.seek(tweets_data_file.tell() - 1, os.SEEK_SET)
    tweets_data_file.truncate()
    
    tweets_data_file.write("]")
    
    tweets_data_file.close()

    print("tweets file generated....")
    return redirect('/dashboard')

def getdashboard(request):
    return render(request,'dashboard.html')