from django.shortcuts import render

def loadHomepage(request):
    return render(request,'index.html')
