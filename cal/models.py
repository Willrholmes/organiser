from django.db import models
from datetime import date
from django.utils import timezone
from django.urls import reverse

class Events(models.Model):
    title = models.CharField(max_length=250)
    start_date = models.DateField(blank=False)
    start_time = models.TimeField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=250, blank=True)
    attendees = models.EmailField(blank=True)
    private = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('cal:viewevent', args=[str(self.id)], current_app='cal')
