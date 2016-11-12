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

def print_premise(object):
    html_text = object.sentence
    return html_text

def print_argument(object):
    return print_aim(object.choice_heading, object.aim_str) + print_premise(object.conclusion)

def print_aim(choice_heading, aim):
    return "<span class=\"aim-" + aim + "\">" + choice_heading + ":</span> "

def print_what(what, aim):
    return "<span class=\"what-" + aim + "\">" + what + ":</span> "

@register.filter
def print_head(object):
    if type(object) == Premise:
        return mark_safe(print_premise(object))
    else:
        return mark_safe(print_argument(object))

@register.filter
def print_link(object):
    url = reverse(object.namespace + ':detail', args = [object.id])
    html = '<a class=\"object_link\" href=\"' + url + '\">'
    if type(object) == Premise:
        return mark_safe(html + print_premise(object) + '</a>')
    else:
        return mark_safe(html + print_argument(object) + '</a>')
