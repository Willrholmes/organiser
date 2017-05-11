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
    #If month/year supplied return calendar for that date.
    else:
        _date = date(int(year), int(month), 1)
    #User backend function to return dictionary required for calendar template.
    #tag.
    cal = calendar(_date, request)
    return render(request, 'calendar.html', cal)

def newevent(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = EventForm(data=request.POST)
            #Use backend.date_format function to format date for calendar.
            date = date_format(form)
            #Pass that info into the backend.calendar function.
            cal = calendar(date, request)
            if form.is_valid():
                event = form.save(commit=False)
                #Add creator from request data
                event.creator = request.user
                #Add end date if not supplied user backend function.
                event.end_date = add_end_date(event.end_date, event.start_date)
                form.save()
                #Use reverse to pull calendar view for the month the event
                #was created for
                return HttpResponseRedirect(reverse('cal:another-month', args=[
                    cal['month'], cal['year']], current_app='cal'))
        else:
            form = EventForm(request.user.username)
            return render(request, 'event.html', {'form': form})
    else:
        #If user not logged in an error message will be displayed.
        messages.warning(request, "Please login to create an event!",
            extra_tags="event-error")
    return redirect('cal:home')

def viewevent(request, id):
    #Receive ID from template/URL and pull correct event from db.
    instance = Events.objects.get(id=id)
    #Use backend.user_or_attendee function to check user can view/edit event.
    if user_or_attendee(request.user, instance):
        if request.method == 'POST':
            form = EventForm(data=request.POST, instance=instance)
            #Use backend.date_format function to format date for calendar.
            date = date_format(form)
            #Pass that info into the backend.calendar function.
            cal = calendar(date, request)
            if form.is_valid():
                event = form.save(commit=False)
                #Add creator from request data
                event.creator = request.user
                #Add end date if not supplied user backend function.
                event.end_date = add_end_date(event.end_date, event.start_date)
                form.save()
                #Use reverse to pull calendar view for the month the event
                #was created for
                return HttpResponseRedirect(reverse('cal:another-month', args=[
                    cal['month'], cal['year']], current_app='cal'))
        else:
            form = EventForm(request.user.username,
                instance=instance)
        return render(request, 'view_event.html', {'form':form, 'id':id})
    else:
        #If user not logged in an error message will be displayed.
        messages.error(
            request, "You do not have permission to see this event",
            extra_tags="event-error")
        return redirect('cal:home')


def delete_event(request, id):
    #Check object can be pulled from db/exists.
    instance = get_object_or_404(Events, id=id)
    #Check user has permission to delete event.
    if user_or_attendee(request.user, instance):
        #Pull date so it can be passed as variables to calendar view.
        date = instance.start_date
        instance.delete()
    #Use reverse to pull calendar view for the month the event was on.
    return HttpResponseRedirect(reverse('cal:another-month', args=[
        date.month, date.year], current_app='cal'))
