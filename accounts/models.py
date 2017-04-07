from django.db import models
from cal.models import Events
import uuid

class Accounts(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(null=False, unique=True)
    password = models.CharField(null=False, max_length=254)
    friends = models.ManyToManyField("self")
    username = models.CharField(max_length=254, null=True)
    events = models.ForeignKey(Events, null=True)
