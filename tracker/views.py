from django.shortcuts import render
from .auth import *

# Create your views here.
def home(request):
    return render(request,'tracker/home.html')