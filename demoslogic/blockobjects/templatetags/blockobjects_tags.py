import json

from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe
from django.template import Library
from django.utils.html import conditional_escape
from django.core.urlresolvers import reverse

from demoslogic.premises.models import Premise
from demoslogic.arguments.models import Argument

register = Library()

def jsonify(object):
    if isinstance(object, QuerySet):
        return mark_safe(serialize('json', object))
    return mark_safe(json.dumps(object))

register.filter('jsonify', jsonify)
jsonify.is_safe = True

def get_premise(object):
    return object.sentence

def get_argument(object):
    return object.conclusion.get_premise_choice(object.aim)

@register.filter
def print_head(object):
    if type(object) == Premise:
        return mark_safe(get_premise(object))
    elif type(object) == Argument:
        return mark_safe(get_argument(object))
    else:
        return mark_safe(str(object))

@register.filter
def print_link(object):
    url = reverse(object.namespace + ':detail', args = [object.id])
    html = '<a class=\"object_link\" href=\"' + url + '\">'
    if type(object) == Premise:
        return mark_safe(html + get_premise(object) + '</a>')
    elif type(object) == Argument:
        return mark_safe(html + get_argument(object) + '</a>')
    else:
        return mark_safe(html + str(object) + '</a>')

@register.filter
def print_thesis(object, thesis_id):
    url = reverse(object.namespace + ':detail', args = [object.id])
    html = '<a class=\"object_link\" href=\"' + url + '\">' + object.get_premise_choice(thesis_id) + '</a>'
    return mark_safe(html)
