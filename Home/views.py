from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User , auth
from django.contrib import messages

def index(request):
    return render(request,"index.html",{"name":"pravin"})

def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        print(username,password)

        user  = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return render(request,'index.html',{'user':user})
            
        else:
            messages.info(request,"Invalid Username or Password")
            return redirect('/login')    
    else:
        return render(request,'login.html')

def signup(request):

    if request.method == 'POST' :
        
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username = username).exists():
            messages.info(request,"Username is already taken !")
        elif User.objects.filter(email = email).exists():
            messages.info(request,"Email id already registered !")
        else:
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()
            return render(request,'index.html')

        return redirect('/signup')
    else:
        return render(request,"signup.html")

def logout(request):
    auth.logout(request)
    return redirect("/index")