from django.forms import ModelForm, DateField
from cal.models import Events
from datetime import date
from django import forms

class EventForm(ModelForm):
    start_date = forms.DateField(widget = forms.DateInput(format="%d/%m/%Y"),
        input_formats=["%d/%m/%Y",], initial=date.today)
    #user = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Events
        exclude = ['created', 'user']
        labels = {'private':"Private?"}
