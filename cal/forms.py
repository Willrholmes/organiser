from django.forms import ModelForm, DateField
from bootstrap_datepicker.widgets import DatePicker
from cal.models import Events
from accounts.models import Account
from django.contrib.auth.models import User
from datetime import date
from django import forms

class EventForm(ModelForm):
    #Meta class allows specification of which model fields required in form
    class Meta:
        model = Events
        exclude = ['created', 'creator', 'private']
        #Widgets allows us to add attributes to HTML for form
        widgets = {'title':forms.TextInput(attrs={'class':'form-control'}),
            'start_time':forms.TimeInput(attrs={
                'class':'datetimepicker3 form-control mb-2 mr-sm-2 mb-sm-0'}),
            'end_time':forms.TimeInput(attrs={
                'class':'datetimepicker3 form-control mb-2 mr-sm-2 mb-sm-0'}),
            'location':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control',
                'rows':10,
                'cols':64
            }),
        }

    #These are declared separately as a number of attributes need to be added.
    #This includes the datetimepicker class which user Jquery to display
    #Bootstrap datetimepicker.
    start_date = forms.DateField(widget = forms.DateInput(
        format="%d/%m/%Y",
        attrs={'class': 'datetimepicker4 form-control mb-2 mr-sm-2 mb-sm-0'}),
        input_formats=["%d/%m/%Y",],
        initial=date.today)

    end_date = forms.DateField(widget = forms.DateInput(
        attrs={'class': 'datetimepicker4 form-control mb-2 mr-sm-2 mb-sm-0'},
        format="%d/%m/%Y"),
        input_formats=["%d/%m/%Y",],
        required=False)

    #Sets up form class to take data (the user) from that is passed into the
    #view from the template and use that to pull the user's friends from the db.
    #This allows us to display the friends as tickbox options in the event form.
    def __init__(self, user=None, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['attendees'] = forms.ModelMultipleChoiceField(
                        queryset=Account.objects.get(username=user).friends,
                        widget=forms.CheckboxSelectMultiple,
                        required=False,
                        )
