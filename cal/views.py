from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from datetime import date, datetime
from django.contrib import messages
from django.views.generic import DeleteView
from cal.forms import EventForm
from django.contrib.auth.models import User
from cal.models import Events
from accounts.models import Account
from cal.backend import calendar, date_format, user_or_attendee, add_end_date

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
            cal = calendar(date, request)
            if form.is_valid():
                event = form.save(commit=False)
                event.creator = request.user
                event.end_date = add_end_date(event.end_date, event.start_date)
                form.save()
                return HttpResponseRedirect(reverse('cal:another-month', args=[
                    cal['month'], cal['year']], current_app='cal'))
        else:
            form = EventForm(request.user.username)
            return render(request, 'event.html', {'form': form})
    else:
        messages.warning(request, "Please login to create an event!",
            extra_tags="event-error")
    return redirect('cal:home')

def viewevent(request, id):
    instance = Events.objects.get(id=id)
    if user_or_attendee(request.user, instance):
        if request.method == 'POST':
            form = EventForm(data=request.POST, instance=instance)
            date = date_format(form)
            cal = calendar(date, request)
            if form.is_valid():
                event = form.save(commit=False)
                event.creator = request.user
                event.end_date = add_end_date(event.end_date, event.start_date)
                form.save()
                return HttpResponseRedirect(reverse('cal:another-month', args=[
                    cal['month'], cal['year']], current_app='cal'))
        else:
            form = EventForm(request.user.username,
                instance=instance)
        return render(request, 'view_event.html', {'form':form, 'id':id})
    else:
        messages.error(
            request, "You do not have permission to see this event",
            extra_tags="event-error")
        return redirect('cal:home')


def delete_event(request, id):
    instance = get_object_or_404(Events, id=id)
    if user_or_attendee(request.user, instance):
        date = instance.start_date
        cal = calendar(date, request)
        instance.delete()
    return HttpResponseRedirect(reverse('cal:another-month', args=[
        date.month, date.year], current_app='cal'))
