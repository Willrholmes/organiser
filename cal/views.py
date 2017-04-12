from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from datetime import date, datetime
from django.contrib import messages
from cal.forms import EventForm
from django.contrib.auth.models import User
from cal.models import Events
from accounts.models import Account
from cal.backend import calendar, date_format, user_or_attendee

def home(request, month=None, year=None):
    if month == None:
        _date = datetime.now()
    else:
        _date = date(int(year), int(month), 1)
    title = "%s %s" % (_date.strftime("%B"), _date.strftime("%Y"))
    cal = calendar(_date, request)
    cal['title'] = title
    return render(request, 'calendar.html', cal)

def newevent(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = EventForm(data=request.POST)
            date = date_format(form)
            cal_title = "%s %s" % (date.strftime("%B"), date.strftime("%Y"))
            cal = calendar(date, request)
            cal['title'] = cal_title
            if form.is_valid():
                event = form.save(commit=False)
                event.creator = request.user
                form.save()
                return redirect('cal:home')
        else:
            form = EventForm(request.user.username)
            return render(request, 'event.html', {'form': form})
    else:
        messages.warning(request, "Please login to create an event!",
            extra_tags="event-error")
    return HttpResponse(str(form.errors))
    #return redirect('cal:home')

def viewevent(request, id):
    instance = Events.objects.get(id=id)
    if user_or_attendee(request.user, instance):
        if request.method == 'POST':
            form = EventForm(data=request.POST, instance=instance)
            date = date_format(form)
            title = "%s %s" % (date.strftime("%B"), date.strftime("%Y"))
            cal = calendar(date, request)
            cal['title'] = title
            if form.is_valid():
                event = form.save(commit=False)
                event.creator = request.user
                form.save()
                return redirect('cal:home')
        else:
            form = EventForm(request.user.username,
                instance=instance)
        return render(request, 'view_event.html', {'form':form})
    else:
        messages.error(
            request, "You do not have permission to see this event",
            extra_tags="event-error")
        return redirect('cal:home')
