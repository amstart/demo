import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone
from vote.managers import VotableManager


class Premise(models.Model):
    subject = models.CharField(default='', max_length=200)
    predicate = models.CharField(default='', max_length=200)
    object = models.CharField(default='', max_length=100)
    complement = models.CharField(default='', max_length=200)

    pub_date = models.DateTimeField('date published')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __init__(self, *args, **kwargs):
        super(Premise,self).__init__(*args, **kwargs)
        self.pub_date = timezone.now()

    def __str__(self):
        return self.subject

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    votes = VotableManager()

class Choice(models.Model):
    question = models.ForeignKey(Premise, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
#choice has a meta class with the ForeignKey and some API, and the base classes with their specific set of choices
#premises and arguments also might share a meta class
