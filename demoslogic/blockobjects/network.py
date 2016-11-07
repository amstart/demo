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
        node['group'] = 1
        node['id'] = 'p' + str(node['id'])
    arguments_qs = Argument.objects.values('id', 'premise1', 'premise2', 'conclusion', 'aim')
    arguments = [entry for entry in arguments_qs]
    links = []
    for argument in arguments:
        node_id = 'a' + str(argument['id'])
        nodes.append({'id': node_id, 'group': 2, 'object': str(argument['aim'])})
        links.append({'source': 'p' + str(argument['premise1']), 'target': node_id, 'value': 2})
        links.append({'source': 'p' + str(argument['premise2']), 'target': node_id, 'value': 2})
        links.append({'source': node_id, 'target': 'p' + str(argument['conclusion']), 'value': 1})
    savedict = {'nodes': nodes, 'links': links}
    save_data(savedict, 'network')
