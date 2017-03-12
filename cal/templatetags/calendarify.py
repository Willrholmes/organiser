from django import template
from calendar import HTMLCalendar
import datetime
from django import template
from itertools import groupby

from django.utils.html import conditional_escape as esc

register = template.Library()

def do_month_calendarify(parser, token):
    # Take the tag input from the template and format
    # Template syntax is {% calendarify year month %}
    try:
        tag_name, year, month = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument formatted as strftime" %
                token.contents.split()[0]
        )
    return CalendarifyNode(year, month)

class CalendarifyNode(template.Node):

    def __init__(self, year, month):
        try:
            self.year = template.Variable(year)
            self.month = template.Variable(month)
        except ValueError:
            raise template.TemplateSyntaxError

    def render(self, context):
        try:
            my_year = self.year.resolve(context)
            my_month = self.month.resolve(context)
            return HTMLCalendar().formatmonth(
                int(my_year), int(my_month), withyear=True)
        except ValueError:
            return "%s, %s" % (my_month, my_year)

register.tag('calendarify', do_month_calendarify)
