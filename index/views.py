from django.shortcuts import render
from django.conf import settings

def index(request):
    context = {
        'session_cookie_age': settings.SESSION_COOKIE_AGE,
    }
    return render(request,'index.html',context)