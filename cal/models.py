from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import Account

class Events(models.Model):
    title = models.CharField(max_length=250)
    start_date = models.DateField(blank=False)
    start_time = models.TimeField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1, related_name='creator')
    created = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=250, blank=True)
    attendees = models.ManyToManyField(
        Account, related_name='attendees', blank=True)
    private = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('cal:viewevent', args=[str(self.id)], current_app='cal')
