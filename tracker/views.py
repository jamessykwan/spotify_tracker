from django.shortcuts import render
from .auth import *

# Create your views here.
def home(request):
    context={
        'auth_url':auth_url
    }
    return render(request,'tracker/home.html',context)