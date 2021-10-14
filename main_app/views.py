from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request,'login.html')

def homepage(request):
    return render(request,'homepage.html')

def request(request):
    return render(request,'request.html')

def clinic(request):
    return render(request,'clinic.html')

def settings(request):
    return render(request,'settings.html')

