from django.contrib.auth.models import Permission, User
from django.db import models

class UserProfile(models.Model):
    #friends = models.ManyToManyField(User, related_name='friends')
    friends = models.ManyToManyField('self', null=True)

