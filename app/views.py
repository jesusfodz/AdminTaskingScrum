from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, "app/index.html")  

def signin(request):
    return render(request, "app/signin.html")    

def register(request):
    return render(request, "app/register.html")     