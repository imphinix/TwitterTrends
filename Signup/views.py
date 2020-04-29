from django.shortcuts import render

def loadSignupPage(request):
    return render(request,'signup.html')