import datetime

from django.db.models.signals import post_save, post_save
from django.dispatch import receiver
from django.conf import settings
from django.db import models
from django.utils import timezone

from .network import save_network

class BlockObject(models.Model):
    pub_date = models.DateTimeField('date published', default = timezone.now)
    staged = models.DateTimeField(null = True, blank = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        abstract = True
        get_latest_by = 'pub_date'

    def __init__(self, *args, **kwargs):
        super(BlockObject,self).__init__(*args, **kwargs)
        if self.staged is None and not self.was_published_recently():
            self.staged = timezone.now()
            self.save()

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days = 1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class NetworkObject(BlockObject):
    class Meta:
        abstract = True

# @receiver(post_save, sender=NetworkObject)
# def model_post_save(sender, **kwargs):
#     save_network()
#
# @receiver(post_delete, sender=NetworkObject)
# def model_post_save(sender, **kwargs):
#     save_network()

class VoteManager(models.Manager):
    pass


class VoteBase(BlockObject):
    objects = VoteManager
    last_voted = models.DateTimeField('last voted', default = timezone.now)

    class Meta:
        abstract = True

    def get_plot_data(self, voteobjects_all):
        vote_number = []
        choices = self._meta.get_field('value').choices
        values = [x[0] for x in choices]
        for value in values:
            vote_number.append(sum(vote.value == value for vote in voteobjects_all))
            max_vote_number = max(vote_number)
        labels = [x[1] for x in choices]
        plot_data = []
        for index, value in enumerate(values):
            item = {'label': labels[index],
                    'bar_width': max([15, vote_number[index]/max_vote_number*350]),
                    'bar_text': str(vote_number[index])}
            plot_data.append(item)
        plot_data[self.value-1]['bar_text'] += " (you)"
        return plot_data

    def update(self, new_value):
        old_value = self.value
        old_last_voted = self.last_voted
        try:
            self.value = new_value
            self.last_voted = timezone.now()
            self.full_clean()
            return self.save()
        except Exception as e:
            print('%s' % (type(e)))
            print(e)
            self.value = old_value
            self.last_voted = old_last_voted
# class Source(BlockObject):
#     source = Charfield(max_length = 200)
    #can be voted on
