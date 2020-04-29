from django.shortcuts import render
import re , string
import pandas as pd
import json
import os
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.corpus import twitter_samples
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer

def lemmatize_sentence(tokens):
    
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []
    
    for word, tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    
    return lemmatized_sentence
    
def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    
    return cleaned_tokens
    
def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token


def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

def getSentiment(): 

    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')
    neutral_tweets  = twitter_samples.strings('tweets.20150430-223406.json')

    #simple tokenizing
    #print(tweet_tokens[0])

    #tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    stop_words = stopwords.words('english')
    #print(remove_noise(tweet_tokens[0], stop_words))

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    all_pos_words = get_all_words(positive_cleaned_tokens_list)

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    import random

    positive_dataset = [(tweet_dict, "Positive")
                     for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                     for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)

    train_data = dataset[:7000]
    test_data = dataset[7000:]

    from nltk import classify
    from nltk import NaiveBayesClassifier
    classifier = NaiveBayesClassifier.train(train_data)

    print("Accuracy is:", classify.accuracy(classifier, test_data))

    print(classifier.show_most_informative_features(10))


    from nltk.tokenize import word_tokenize

    #custom_tweet = "life is good"

    BASE_DIR = 'C:\\Users\\BURPY\\Desktop\\TwitterTrends\\'
    path = BASE_DIR + 'Data/tweets_data.txt'

    tweets_data = []
    try:
        with open(path,'r') as json_obj:
            tweets_data = json.loads(json_obj.read())
    except Exception as e:
        print("Error",e)
    
    tweets = pd.DataFrame()

    tweets['text'] = [tweet.get('text','') for tweet in tweets_data]

    positive_count = 0
    negative_count = 0

    for tweet in tweets_data:
        custom_tweet = tweet.get('text','')    
        custom_tokens = remove_noise(word_tokenize(custom_tweet))
        polarity = classifier.classify(dict([token, True] for token in custom_tokens))
    
        if polarity == "Positive":
            positive_count = positive_count + 1
        else:
            negative_count = negative_count + 1
    
    # data = getCountData()
    # return render(request,'dashboard.html',{'pv':positive_count,'nv':negative_count,'total_post':data[0],'total_user':data[1],'total_reach':data[2]})

    return (positive_count,negative_count)

def loadDashboard(request):
    return render(request,'dashboard.html')