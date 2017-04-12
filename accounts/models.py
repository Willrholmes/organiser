from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

#Extension of User model to allow a user to have 'friends' via a ManyToManyField
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(
        'self', related_name=user)
    username = models.CharField(max_length=100, null=True)

#Allows returned object to be seen as username
    def __str__ (self):
        return self.username

#Ensure an Account object is made whenever a User object is made
@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    if kwargs.get("created", False):
        Account.objects.get_or_create(user=kwargs.get('instance'),
                username=kwargs.get('instance').username)
