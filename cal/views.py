from django.shortcuts import render, redirect
import datetime

def home(request):
    title = "Welcome To The Calendar Home Page"
    month = str(datetime.datetime.now().strftime("%m"))
    year = str(datetime.datetime.now().strftime("%Y"))
    return render(request, 'home.html', {'month':month, 'year':year, 'title':title})
