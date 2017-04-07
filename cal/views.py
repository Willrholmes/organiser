from django.shortcuts import render, redirect, HttpResponse
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from datetime import date, datetime
from cal.forms import EventForm
from cal.models import Events
from cal.backend import monthdict, calendar
from django.forms.models import model_to_dict

def home(request, month=None, year=None):
    user = request.user.get_username()
    if month == None:
        _date = datetime.now()
    else:
        _date = date(int(year), int(month), 1)
    title = "%s %s" % (_date.strftime("%B"), _date.strftime("%Y"))
    return render(request, 'calendar.html', calendar(_date, title))

def newevent(request):
    user = request.user.get_username()
    if request.method == 'POST':
        form = EventForm(request.POST)
        _date = form.data['start_date'].split("/")
        a = [int(i) for i in _date]
        _date_ = date(a[2], a[1], a[0])
        if form.is_valid():
            form.save(commit=True)
            return render(request, 'calendar.html', calendar(_date_))
    else:
        form = EventForm()
    return render(request, 'event.html', {'form': form})

def viewevent(request, id):
    user = request.user.get_username()
    instance = Events.objects.get(id=id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=instance)
        _date = form.data['start_date'].split("/")
        a = [int(i) for i in _date]
        _date_ = date(a[2], a[1], a[0])
        if form.is_valid():
            form.save()
            return redirect('cal:home')
    else:
        form = EventForm(instance=instance)
    return render(request, 'view_event.html', {'form':form})
