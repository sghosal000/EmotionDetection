from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home/home.html');

def login(request):
    context={
        "pname":"login",
    }
    return render(request,'home/login.html',context)
def signup(request):
    context={
        "pname":"signup",
    }
    return render(request,'home/signup.html',context)

