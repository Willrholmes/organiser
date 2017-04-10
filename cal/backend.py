from datetime import date, datetime
from calendar import monthrange
from cal.models import Events

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

def calendar(_date, request):
    date_dict = monthdict(_date)
    from_month_date = date(date_dict['year'], date_dict['month'], 1)
    to_month_date = date(date_dict['year'], date_dict['month'], monthrange(
        date_dict['year'], date_dict['month'])[1])
    user = request.user
    if user.is_authenticated:
        event_list = Events.objects.filter(user=user).filter(
            start_date__gte=str(from_month_date)).filter(start_date__lte=str(
            to_month_date))
    else:
        event_list = Events.objects.filter(user=None).filter(
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
