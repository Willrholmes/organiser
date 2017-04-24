from django.forms import ModelForm, DateField
from bootstrap_datepicker.widgets import DatePicker
from cal.models import Events
from accounts.models import Account
from django.contrib.auth.models import User
from datetime import date
from django import forms

class EventForm(ModelForm):

    class Meta:
        model = Events
        exclude = ['created', 'creator', 'private']
        widgets = {'title':forms.TextInput(attrs={'class':'form-control'}),
            'start_time':forms.TimeInput(attrs={
                'class':'datetimepicker3 form-control'}),
            'end_time':forms.TimeInput(attrs={
                'class':'datetimepicker3 form-control'}),
            'location':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),
        }

    start_date = forms.DateField(widget = forms.DateInput(
        format="%d/%m/%Y",
        attrs={'class': 'datetimepicker4 form-control'}),
        input_formats=["%d/%m/%Y",],
        initial=date.today)
    end_date = forms.DateField(widget = forms.DateInput(
        attrs={'class': 'datetimepicker4 form-control'},
        format="%d/%m/%Y"),
        input_formats=["%d/%m/%Y",],
        required=False)

    def __init__(self, user=None, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['attendees'] = forms.ModelMultipleChoiceField(
                        queryset=Account.objects.get(username=user).friends,
                        widget=forms.CheckboxSelectMultiple,
                        required=False,
                        )
