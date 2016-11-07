import json
import os

from django.core import serializers
from config.settings.common import APPS_DIR
from demoslogic.arguments.models import Argument
from demoslogic.premises.models import Premise

def save_data(data, filename = 'data'):
    filename = os.path.join(str(APPS_DIR), 'static/json/' + filename + '.json')
    with open(filename, 'w') as fp:
        json.dump(data, fp)

def save_network():
    statements_qs = Premise.objects.values('id', 'object')
    nodes = [entry for entry in statements_qs]
    for node in nodes:
        node['group'] = node['id']
    arguments_qs = Argument.objects.values('id', 'premise1', 'premise2', 'conclusion')
    argument_connectors = [entry for entry in arguments_qs]
    links = []
    for connector in argument_connectors:
        links.append({'source': connector['premise1'], 'target':connector['conclusion'], 'value': connector['id']})
        links.append({'source': connector['premise2'], 'target':connector['conclusion'], 'value': connector['id']})
    savedict = {'nodes': nodes, 'links': links, 'argument_connectors': argument_connectors}
    save_data(savedict, 'network')
