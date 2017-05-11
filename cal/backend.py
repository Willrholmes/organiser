from datetime import date, datetime
from calendar import monthrange
from cal.models import Events
from itertools import chain
from django.contrib.auth.models import User
from accounts.models import Account

#Will return a dictionary with all the information required for naviation
#between months on the calendar homepage.
def monthdict(_date):
    month, year = _date.month, _date.year
    next_month = month + 1
    last_month = month - 1
    last_year = year
    next_year = year
    if month == 12:
        next_month = 1
        next_year = year + 1
    if month == 1:
        last_month = 12
        last_year = year - 1
    return {
    'month':month,
    'year':year,
    'last_month':last_month,
    'last_year':last_year,
    'next_month':next_month,
    'next_year':next_year,
    }

#Will return a dictionary with all the information required to produce a
#calendar homepage with buttons required for easy navigation.
def calendar(_date, request):
    date_dict = monthdict(_date)
    from_month_date = date(date_dict['year'], date_dict['month'], 1)
    to_month_date = date(date_dict['year'], date_dict['month'], monthrange(
        date_dict['year'], date_dict['month'])[1])
    user = request.user
    #Pulls a list of events for a given user on a given month - whether they
    # be the creator of the event or an attendee.
    if user.is_authenticated:
        event_list_1 = Events.objects.filter(creator=user).filter(
            end_date__gte=str(from_month_date)).filter(start_date__lte=str(
            to_month_date))
        attendee = Account.objects.get(user=user)
        event_list_2 = Events.objects.filter(attendees=attendee).filter(
            end_date__gte=str(from_month_date)).filter(start_date__lte=str(
            to_month_date))
        event_list = list(chain(event_list_1, event_list_2))
    else:
        event_list = Events.objects.filter(creator=None).filter(
            start_date__gte=str(from_month_date)).filter(start_date__lte=str(
            to_month_date))
    return {
        'month':date_dict['month'],
        'year':date_dict['year'],
        'event_list':event_list,
        'lastmonth':date_dict['last_month'],
        'lastyear':date_dict['last_year'],
        'nextmonth':date_dict['next_month'],
        'nextyear':date_dict['next_year'],
        }

#Format date provided in form to allow correct format to be passed into above
#functions.
def date_format(form):
    _date = form.data['start_date'].split("/")
    a = [int(i) for i in _date]
    _date_ = date(a[2], a[1], a[0])
    return _date_

#Check if a given user is the creator of or attending an event.
def user_or_attendee(user, instance):
    if instance.creator == user:
        return True
    for e in instance.attendees.all():
        print(e, user.username)
        if str(e) == str(user.username):
            return True
    else:
        return False

#Add and end date if specified in form.
def add_end_date(end_date, start_date):
    if end_date == None:
        return str(start_date)
    else:
        return str(end_date)
