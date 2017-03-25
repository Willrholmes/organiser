from django import template
from calendar import HTMLCalendar
from datetime import date
from django import template
from itertools import groupby

from django.utils.html import conditional_escape as esc

register = template.Library()

def do_month_calendarify(parser, token):
    # Take the tag input from the template and format
    # Template syntax is {% calendarify year month %}
    try:
        tag_name, year, month, event_list = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires three arguments" % token.contents.split()[0]
        )
    return CalendarifyNode(year, month, event_list)

class CalendarifyNode(template.Node):

    def __init__(self, year, month, event_list):
        try:
            self.year = template.Variable(year)
            self.month = template.Variable(month)
            self.event_list = template.Variable(event_list)
        except ValueError:
            raise template.TemplateSyntaxError

    def render(self, context):
        try:
            my_year = self.year.resolve(context)
            my_month = self.month.resolve(context)
            my_event_list = self.event_list.resolve(context)
            cal = EventCalendar(my_event_list)
            return cal.formatmonth(
                int(my_year), int(my_month))
        except ValueError:
            return "%s, %s, %s" % (my_month, my_year, my_event_list)

class EventCalendar(HTMLCalendar):
    # Use Python's HTMLCalendar and put user events over top
    def __init__(self, events):
        super(EventCalendar, self).__init__()
        self.events = self.group_by_day(events)

    def formatday(self, day, weekday):
        if day != 0:
            cssid = self.cssclasses[weekday]
            cssclass = "daybox"
            if date.today() == date(self.year, self.month, day):
                cssid += ' today'
            if day in self.events:
                cssid += ' filled'
                body = ['<ul>']
                for event in self.events[day]:
                    body.append('<li>')
                    body.append('<a href="/%s/">' % event.title)
                    body.append(esc(event.title))
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(
                    cssclass, cssid, '<span class="dayNumber">%d</span> %s' % (
                        day, ''.join(body)))
            return self.day_cell(
                cssclass, cssid, '<span class="dayNumberNoReadings">%d</span>' % (day))
        return self.day_cell('nodaybox', 'noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(EventCalendar, self).formatmonth(year, month)

    def group_by_day(self, events):
        field = lambda event: event.start_date.day
        return dict(
            [(day, list(items)) for day, items in groupby(events, field)]
        )

    def day_cell(self, cssclass, cssid, body):
        return '<td class="%s" id="%s">%s</td>' % (cssclass, cssid, body)

register.tag('calendarify', do_month_calendarify)
