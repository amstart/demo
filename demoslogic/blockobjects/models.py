import datetime

from django.core import serializers
from django.conf import settings
from django.db import models
from django.utils import timezone

class BlockObject(models.Model):
    pub_date = models.DateTimeField('date published', default = timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        abstract = True

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days = 1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class NetworkObject(BlockObject):
    staged = models.DateTimeField(null = True, blank = True)

    def __init__(self, *args, **kwargs):
        super(NetworkObject,self).__init__(*args, **kwargs)
        if self.staged is None and not self.was_published_recently():
            self.staged = timezone.now()
            self.save()

    def save(self, *args, **kwargs):
        super(NetworkObject, self).save(*args, **kwargs)
        self.save_network()

    def delete(self, *args, **kwargs):
        super(NetworkObject, self).delete(*args, **kwargs)
        self.save_network()

    def save_data(self, data, filename = 'data'):
        import json
        import os
        from config.settings.common import APPS_DIR
        filename = os.path.join(str(APPS_DIR), 'static/json/' + filename + '.json')
        with open(filename, 'w') as fp:
            json.dump(data, fp)

    def save_network(self):
        from demoslogic.arguments.models import Argument
        from demoslogic.premises.models import Premise
        arguments_qs = Argument.objects.values('id', 'premise1', 'premise2', 'conclusion',
                                               'aim', 'premise1_if', 'premise2_if')
        arguments = [entry for entry in arguments_qs]
        statements_qs = Premise.objects.values('id', 'sentence')
        nodes = [entry for entry in statements_qs]
        for node in nodes:
            node['group'] = 1
            node['id'] = 'p' + str(node['id'])
            node['name'] = node.pop('sentence')
            # node['related_conclusions'] =
            # node['related_premises'] =
            # node['related_argument'] =
        links = []
        for argument in arguments:
            node_id = 'a' + str(argument['id'])
            nodes.append({'id': node_id, 'group': 2, 'name': ''})
            links.append({'source': 'p' + str(argument['premise1']), 'target': node_id,
                          'value': 2, 'aim': argument['premise1_if']})
            links.append({'source': 'p' + str(argument['premise2']), 'target': node_id,
                          'value': 2, 'aim': argument['premise2_if']})
            links.append({'source': node_id, 'target': 'p' + str(argument['conclusion']),
                          'value': 1, 'aim': argument['aim']})
        savedict = {'nodes': nodes, 'links': links}
        self.save_data(savedict, 'network')

    class Meta:
        abstract = True
        get_latest_by = 'pub_date'


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
        if not choices:
            choices = self.object.choices
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
        plot_data[self.value]['bar_text'] += " (you)"
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
