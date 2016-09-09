from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission, User
from datetime import datetime
# Create your models here.


class Card(models.Model):
    user = models.ForeignKey(User, default=1)

    topic = models.CharField(max_length=200)
    front = models.CharField(max_length=1000)
    back = models.CharField(max_length=1000)

    review_time = models.DateTimeField()
    review_interval = models.BigIntegerField(default=60)    # in seconds

    card_audio = models.CharField(default='', max_length=300)
    card_score = models.CharField(default='', max_length=300)
    card_pic = models.FileField()

    is_new = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('cards:detail', kwargs={'pk': self.pk})

