from django.shortcuts import render
from .sentiment_analysis import sentence_sentiment
from .analysis import analysis
from django.http import JsonResponse
from .analysis.analysis import getCountData , getLanguageData
from random import randint
 
version = str(randint(0,100))

def loadDashboardPage(request):
    
    print(version)

    total_post, total_user, total_reach = getCountData()
    positive_count , negative_count = sentence_sentiment.getSentiment()
        
    return render(request,'dashboard.html',{'pv':positive_count,'nv':negative_count,'total_post':total_post,'total_user':total_user,'total_reach':total_reach,'version':getRandomVersion()})

def getRandomVersion():
    return "1"

# def loadDashboardPage(request):
#     response = sentence_sentiment.getSentiment(request)
#     return response

def loaddemo(request):
    return render(request,'demo.html')

    
def get_data(request):
    
    data = []
    languages , languages_count = analysis.getLanguageData()
    hashtags , hashtags_count = analysis.getHashtagData()   
    rtorgRatio = analysis.getRtOrgRatio()

    data = {
		'hashtags': hashtags[:10],
		'hashtags_count': hashtags_count[:10],
        
        'languages' : languages[:10],
        'languages_count' : languages_count[:10],

        'rtorgRatio':rtorgRatio,
	}
    
    return JsonResponse(data)
