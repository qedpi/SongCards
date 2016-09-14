from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission, User
from datetime import datetime
# Create your models here.

initial_review_interval = 60 * 60 * 12 #seconds: half a day
auto_gen_token = 'auto_generate'

CARD_SCOPE_CHOICES = (
    ('U', "public"),
    ('S', "sharable"),
    ('P', "private")
)

class Card(models.Model):
    user = models.ForeignKey(User, default=1)

    topic = models.CharField(max_length=100, verbose_name='Song Title')
    front = models.CharField(blank=True, default='', max_length=100, verbose_name='Artist Name')
    back = models.TextField(blank=True, default=auto_gen_token, max_length=10000, verbose_name='Lyrics & Tabs')

    review_time = models.DateTimeField()
    review_interval = models.BigIntegerField(default=initial_review_interval)

    card_audio = models.CharField(blank=True, default=auto_gen_token, max_length=300, verbose_name='Youtube Link')
    card_score = models.CharField(blank=True, default=auto_gen_token, max_length=300, verbose_name='Lyrics Link')
    card_pic = models.FileField(blank=True, verbose_name='Cover Picture (auto-generates if empty)')

    is_new = models.BooleanField(default=True)
    is_favorite = models.BooleanField(default=False, verbose_name="Is Favorite")
    is_pinned = models.BooleanField(default=False, verbose_name="Is Pinned")

    date_created = models.DateTimeField(default=datetime.utcnow())

    visibility = models.CharField(max_length=1, choices=CARD_SCOPE_CHOICES, default='S',
                                  verbose_name="Card Privacy Setting")

    def __str__(self):
        return self.topic + ' - ' + self.front

    def get_absolute_url(self):
        return reverse('cards:detail', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ('topic', 'front',)

