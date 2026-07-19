from django.shortcuts import render


def home_page(request):
    return render(request, "home/index.html")

def index(request):
    return render(request, 'home/index.html')

def information_centre(request):
    return render(request, "home/information_centre.html")

def password_security(request):
    return render(request, "home/passwordsecurity.html")

def information_centre(request):
    return render(request, 'home/information_centre.html')

def readmore1(request):
    return render(request, 'home/readmore1.html')
def readmore2(request):
    return render(request, 'home/readmore2.html')
   
def readmore3(request):
    return render(request, 'home/readmore3.html')
   
def readmore4(request):
    return render(request, 'home/readmore4.html')

def readmore5(request):
    return render(request, 'home/readmore5.html')

def readmore6(request):
    return render(request, 'home/readmore6.html') 