import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import validate_comma_separated_integer_list

class BlockObject(models.Model):
    pub_date = models.DateTimeField('date published', default = timezone.now)
    staged = models.DateTimeField(null = True, blank = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        abstract = True

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


class VoteManager(models.Manager):
    pass


class VoteBase(BlockObject):
    objects = VoteManager
    last_voted = models.DateTimeField('last voted', default = timezone.now)

    class Meta:
        abstract = True

    def update(self, new_value):
        old_value = self.value
        try:
            self.value = new_value
            self.full_clean()
            return self.save()
        except Exception as e:
            print('%s' % (type(e)))
            self.value = old_value
# class Source(BlockObject):
#     source = Charfield(max_length = 200)
    #can be voted on
