from django.shortcuts import render

def loadLoginPage(request):
    return render(request,'login.html')