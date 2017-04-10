from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import date, datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cal.forms import EventForm
from cal.models import Events
from cal.backend import calendar

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
            form = EventForm(request.POST)
            _date = form.data['start_date'].split("/")
            a = [int(i) for i in _date]
            _date_ = date(a[2], a[1], a[0])
            cal = calendar(_date, request)
            cal['title'] = title
            if form.is_valid():
                event = form.save(commit=False)
                event.user = request.user
                form.save()
                return render(request, 'calendar.html', cal)
        else:
            form = EventForm()
            return render(request, 'event.html', {'form': form})
    else:
        messages.warning(request, "Please login to create an event!",
                        extra_tags="event-error")
    return redirect('cal:home')

def viewevent(request, id):
    instance = Events.objects.get(id=id)
    if instance.user == request.user:
        if request.method == 'POST':
            form = EventForm(request.POST, instance=instance)
            _date = form.data['start_date'].split("/")
            a = [int(i) for i in _date]
            _date_ = date(a[2], a[1], a[0])
            cal = calendar(_date, request)
            cal['title'] = title
            if form.is_valid():
                form.save()
                return render(request, 'calendar.html', cal)
        else:
            form = EventForm(instance=instance)
        return render(request, 'view_event.html', {'form':form})
    else:
        messages.warning(
            request, "You do not have permission to see this event",
            extra_tags="event-error")
        return redirect('cal:home')
