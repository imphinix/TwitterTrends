from django.urls import path
from . import views
from .fetch_tweets_data import fetch_tweets

urlpatterns = [
    path('fetch_tweets',fetch_tweets.getdata),
    #path('fetch_tweets',fetch_tweets.getdashboard),
    path('index',views.loadHomepage,name="index"),
]