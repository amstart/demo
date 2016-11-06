import json

from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe
from django.template import Library
from django.utils.html import conditional_escape

from demoslogic.premises.models import Premise

register = Library()

def jsonify(object):
    if isinstance(object, QuerySet):
        return mark_safe(serialize('json', object))
    return mark_safe(json.dumps(object))

register.filter('jsonify', jsonify)
jsonify.is_safe = True

def print_premise(object):
    html_text = ""
    for element in object.core_list:
        html_text = html_text + \
                            "<span class=\"" + \
                            element["textclass"] + "\">" + \
                            conditional_escape(element["value"]) + "</span> "
    return mark_safe(html_text)

def print_aim(choice_heading, aim):
    html_text = "<span class=\"aim-" + aim + "\">" + choice_heading + ":</span> "
    return html_text

def print_what(what, aim):
    html_text = "<span class=\"what-" + aim + "\">" + what + ":</span> "
    return html_text

@register.filter
def print_head(object):
    if type(object) == Premise:
        return print_premise(object)
    else:
        html_text = print_aim(object.choice_heading, object.aim_str) + print_premise(object.conclusion)
        return mark_safe(html_text)

@register.filter
def print_body(object):
    if type(object) == Premise:
        return ('')
    else:
        aim = object.aim_str
        what = object.choice_what
        html_premises = 'Premise 1: ' + print_premise(object.premise1) + '<br>' + \
                        'Premise 2: ' + print_premise(object.premise2) + '<br>'
        html_conclusion = 'Because of this, ' + print_what(what, aim) + '<br>' + \
        print_premise(object.conclusion) + '<br>'

        html_text = html_premises + html_conclusion
        return mark_safe(html_text)
