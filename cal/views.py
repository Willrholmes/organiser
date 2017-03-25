from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from datetime import date, datetime
from cal.forms import EventForm
from cal.models import Events
from cal.backend import monthdict, calendar

def home(request, month=None, year=None):
    if month == None:
        _date = datetime.now()
    else:
        _date = date(int(year), int(month), 1)
    title = "%s, %s" % (_date.strftime("%B"), _date.strftime("%Y"))
    return render(request, 'calendar.html', calendar(_date, title))

def newEvent(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        _date = form.data['start_date'].split("/")
        a = [int(i) for i in _date]
        _date_ = date(a[2], a[1], a[0])
        title = "Event saved"
        if form.is_valid():
            form.save(commit=True)
            return render(request, 'calendar.html', calendar(_date_, title))
    else:
        form = EventForm()
    return render(request, 'new_event.html', {'form': form})

def viewEvent(request, title):
    if request.method == 'POST':
        form = EventForm(request.POST)
        date = form.data['start_date']
        month = date[3:5]
        year = date[6:]
        if form.is_valid():
            form.save()
            return render(request, 'home.html', {'month':month, 'year':year})
        else:
            form = Events.objects.get(title=title)
    return render(request, 'view_event.html', {'form':form})
