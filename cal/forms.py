from django.forms import ModelForm, DateField
from cal.models import Events
from accounts.models import Account
from django.contrib.auth.models import User
from datetime import date
from django import forms

class EventForm(ModelForm):

    class Meta:
        model = Events
        exclude = ['created', 'creator', 'private']

    start_date = forms.DateField(widget = forms.DateInput(format="%d/%m/%Y"),
        input_formats=["%d/%m/%Y",], initial=date.today)

    def __init__(self, user=None, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['attendees'] = forms.ModelMultipleChoiceField(
                        queryset=Account.objects.get(username=user).friends,
                        widget=forms.CheckboxSelectMultiple,
                        required=False,
                        )
